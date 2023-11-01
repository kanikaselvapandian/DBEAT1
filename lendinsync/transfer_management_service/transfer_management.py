from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import requests
from invokes import invoke_http
import json

app = Flask(__name__)
CORS(app, resources={r"/transfer": {"origins": "http://localhost"}})

wallet_update_by_wid_URL = "http://localhost:7000/wallet/"
transaction_create_URL = "http://localhost:8000/transaction"

@app.route("/transfer", methods=['POST'])
def create_transfer():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            transfer = request.get_json()
            transfer['AmountTransferred'] = float(transfer["AmountTransferred"])
            transfer['ExchangeRate'] = float(transfer["ExchangeRate"])
            print("\nReceived an order in JSON:", transfer)

            if(transfer.get("WalletTransaction")): #transaction is between wallets
                new_source_amount = {
                    "Amount": float(transfer["AmountTransferred"]),
                    "Type": "Withdrawal"
                }
                update_source_wallet = invoke_http(wallet_update_by_wid_URL + str(transfer['SourceWallet']), method='PUT', json=new_source_amount)
                print("\n\nReceived wallet update result:", update_source_wallet)

                new_destination_amount = {
                    "Amount": float(transfer["AmountTransferred"]) * float(transfer["ExchangeRate"]),
                    "Type": "Deposit"
                }
                update_destination_wallet = invoke_http(wallet_update_by_wid_URL + str(transfer['DestinationWallet']), method='PUT', json=new_destination_amount)
                print("\n\nReceived wallet update result:", update_destination_wallet)

                # transfer['DestinationWallet'] = transfer['SourceWallet']
                # transfer['SourceWallet'] = 0

                result = invoke_http(transaction_create_URL, method='POST', json=transfer)
                print("\n\nReceived transaction creation result:", result)
            
            elif("WalletTransaction" in transfer and not transfer["WalletTransaction"] and transfer.get("SourceWallet") is None):  #transaction is between bank and wallet (deposit)
                new_destination_amount = {
                    "Amount": float(transfer["AmountTransferred"]) * float(transfer["ExchangeRate"])
                }
                update_destination_wallet = invoke_http(wallet_update_by_wid_URL + str(transfer['DestinationWallet']), method='PUT', json=new_destination_amount)
                print("\n\nReceived wallet update result:", update_destination_wallet)

                result = invoke_http(transaction_create_URL, method='POST', json=transfer)
                print("\n\nReceived transaction creation result:", result)
            else:
                new_source_amount = {
                    "Amount": float(transfer["AmountTransferred"]) * float(transfer["ExchangeRate"])
                }
                update_source_wallet = invoke_http(wallet_update_by_wid_URL + str(transfer['SourceWallet']), method='PUT', json=new_source_amount)
                print("\n\nReceived wallet update result:", update_source_wallet)

                result = invoke_http(transaction_create_URL, method='POST', json=transfer)
                print("\n\nReceived transaction creation result:", result)

            return jsonify(result), 200

        except Exception as e:
            raise e
            pass

    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(e)
    }), 400

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__))
    app.run(host="0.0.0.0", port=6100, debug=True)