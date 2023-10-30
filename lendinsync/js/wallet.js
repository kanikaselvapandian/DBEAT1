const customer_id = "A123456";
const get_wallets_by_customerid = "http://127.0.0.1:7000/wallet/" + customer_id;
const get_transactions_by_customerid = "http://127.0.0.1:8000/transaction/" + customer_id;
const create_wallet = "http://127.0.0.1:7000/wallet";
const create_transaction = "http://127.0.0.1:6100/transfer"
const deposit_account = "0000010505"
const deposit_account_balance = "40000"

const wallet = Vue.createApp({
  data() {
    return {
      customer_wallets: [],
      customer_transactions: [],
      wallets_received: false,
      transactions_received: false,
      message: '', // Define a message property for error handling
      data_received: false,
      currency_info: [],
      selectedCurrency: "",
      customer_id: customer_id,
      deposit_account: deposit_account,
      wallet_amount: 0,
      exchange_rate: 0,
      sourcewallet: null,
      destinationwallet: null,
      availableDestinationWallets: [],
      availableSourceWallets: [],
      deposit_account_balance: deposit_account_balance,
      validation_errors: [],
      errorsFound: false,
    };
  },
  methods: {
    async get_wallets() {
      try {
        const response = await fetch(get_wallets_by_customerid);
        const data = await response.json();

        if (data.code === 404) {
          this.message = data.message;
        } else {
          this.customer_wallets = data.data.wallet; 
          this.wallets_received = true;
          this.availableSourceWallets = this.customer_wallets;
          this.availableDestinationWallets = this.customer_wallets;
          this.checkDataReceived();
        }
      } catch (error) {
        this.message = 'Error fetching wallet data: ' + error;
      }
    },
    async get_transactions() {
      try {
        const response = await fetch(get_transactions_by_customerid);
        const data = await response.json();

        if (data.code === 404) {
          this.message = data.message;
        } else {
          this.customer_transactions = data.data.transactions;
          this.transactions_received = true;
          this.checkDataReceived();
        }
      } catch (error) {
        this.message = 'Error fetching transaction data: ' + error;
      }
    },
    checkDataReceived() {
      if (this.wallets_received && this.transactions_received) {
        this.data_received = true;
      }
    },
    async getCurrencyCodes(){
        const response = await fetch('http://tbankonline.com/SMUtBank_API/Gateway?Header={"serviceName": "getCurrencyList", "userID": "", "PIN": "", "OTP": ""}&Content={"baseCurrency": "SGD", "quoteCurrency": "USD"}');
        const data = await response.json();
        this.currency_info = data.Content.ServiceResponse.CurrencyList.Currency;
    },
    async getExchangeRate(currency_code){
        const response = await fetch(`http://tbankonline.com/SMUtBank_API/Gateway?Header={"serviceName": "getExchangeRate", "userID": "", "PIN": "", "OTP": ""}&Content={"baseCurrency": "SGD", "quoteCurrency": "${currency_code}"}`);
        const data = await response.json();
        this.exchange_rate = data.Content.ServiceResponse["FX_SpotRate_Read-Response"]["Rate"];
    },
    updateSourceAndCheck() {
      this.updateSourceWallets();
      this.checkWalletsSelection();
    },
    checkWalletsSelection() {
        console.log("checking")
        if (this.sourcewallet && this.destinationwallet) {
            console.log("checking!")
            this.getWalletExchange();
        }
    },
    async getWalletExchange() {
        console.log("here");
        if (this.sourcewallet && this.destinationwallet) {
            console.log("Both wallets have been selected");
            const response = await fetch(`http://tbankonline.com/SMUtBank_API/Gateway?Header={"serviceName": "getExchangeRate", "userID": "", "PIN": "", "OTP": ""}&Content={"baseCurrency": "${this.sourcewallet.CurrencyCode}", "quoteCurrency": "${this.destinationwallet.CurrencyCode}"}`);
            const data = await response.json();
            console.log(data);
            this.exchange_rate = data.Content.ServiceResponse["FX_SpotRate_Read-Response"]["Rate"];
            console.log(this.exchange_rate);
        } else {
            console.log("Both source and destination wallets need to be chosen.");
        }
    },    
    async createWallet(event) {
        event.preventDefault();
        this.validation_errors = []
        if (this.wallet_amount > this.deposit_account_balance) {
            this.validation_errors.push("Insufficient funds in deposit account");
        }
        if (this.wallet_amount <= 0) {
            this.validation_errors.push("Amount must be greater than 0");
        }
        if (this.selectedCurrency == "") {
            this.validation_errors.push("Please select a currency");
        }
        if (this.validation_errors.length > 0) {
            this.errorsFound = true
            return;
        }
        else {
            this.validation_errors = [];
            this.errorsFound = false;
            const jsonData = JSON.stringify({
              CustomerId: this.customer_id,
              CurrencyCode: this.selectedCurrency,
              Amount: this.wallet_amount * this.exchange_rate
          });
      
          const url = create_wallet;
          const postMethod = {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: jsonData
          };
      
          try {
              const response = await fetch(url, postMethod);
              const data = await response.json();
      
              switch (data.code) {
                  case 201:
                      // Handle success case
                      break;
                  case 500:
                      this.message = data.message;
                      break;
                  default:
                      throw `${data.code}: ${data.message}`;
              }
          } catch (error) {
              console.error('Error');
          }
        }
    },
    createTransaction(WalletTransaction, event) {
      event.preventDefault();
        if (WalletTransaction){
            this.validation_errors = []
            this.errorsFound = false;
            if (this.wallet_amount > this.sourcewallet.Amount) {
              this.validation_errors.push("Insufficient funds in source wallet");
            }
            if (this.wallet_amount <= 0 || this.wallet_amount == "") {
              this.validation_errors.push("Amount must be greater than 0");
            }
            if (this.sourcewallet == null) {  
              this.validation_errors.push("Please select a source wallet");
            }
            if (this.destinationwallet == null) {
              this.validation_errors.push("Please select a destination wallet");
            }
            if (this.validation_errors.length > 0) {
              this.errorsFound = true
              return;
            }
            else {
                this.walletWalletTransaction()
            }
        }
        else if (WalletTransaction == false && this.sourcewallet == deposit_account) {
            this.validation_errors = []
            this.errorsFound = false;
            if (this.wallet_amount > this.deposit_account_balance) {
              this.validation_errors.push("Insufficient funds in deposit account");
            }
            if (this.wallet_amount <= 0 || this.wallet_amount == "") {
              this.validation_errors.push("Amount must be greater than 0");
            }
            if (this.destinationwallet == null) {
              this.validation_errors.push("Please select a destination wallet");
            }
            if (this.validation_errors.length > 0) {
              this.errorsFound = true
              return;
            }
            else {
                this.withdrawWalletTransaction()
            }
        }
        else {
            this.validation_errors = []
            this.errorsFound = false;
            if (this.wallet_amount > this.sourcewallet.Amount) {
              this.validation_errors.push("Insufficient funds in source wallet");
            }
            if (this.wallet_amount <= 0 || this.wallet_amount == "") {
              this.validation_errors.push("Amount must be greater than 0");
            }
            if (this.destinationwallet == null) {
              this.validation_errors.push("Please select a destination wallet");
            }
            if (this.validation_errors.length > 0) {
              this.errorsFound = true
              return;
            }
            else {
              this.depositWalletTransaction()
            }
        }
    }},
    async walletWalletTransaction() {
      const jsonData = JSON.stringify({
        SourceWallet: this.sourcewallet.WID,
        DestinationWallet: this.destinationwallet.WID,
        CustomerId: this.customer_id,
        WalletTransaction: true,
        ExchangeRate: this.exchange_rate,
        TimeStamp: new Date(),
        AmountTransferred: this.wallet_amount * this.exchange_rate
        });
        const url = create_transaction;
        const postMethod = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonData
        };
    
        try {
            const response = await fetch(url, postMethod);
            const data = await response.json();
    
            switch (data.code) {
                case 201:
                    // Handle success case
                    break;
                case 500:
                    this.message = data.message;
                    break;
                default:
                    throw `${data.code}: ${data.message}`;
            }
        } 
        catch (error) {
            console.error('Error:', error);
            // Handle other errors or display a general error message
        }
    },
    async depositWalletTransaction() {
        const jsonData = JSON.stringify({
        SourceWallet: this.sourcewallet.WID,
        DestinationWallet: null,
        CustomerId: this.customer_id,
        WalletTransaction: false,
        ExchangeRate: this.exchange_rate,
        TimeStamp: new Date(),
        AmountTransferred: this.wallet_amount * this.exchange_rate
        });

        const url = create_transaction;
        const postMethod = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonData
        };
    
        try {
            const response = await fetch(url, postMethod);
            const data = await response.json();
    
            switch (data.code) {
                case 201:
                    // Handle success case
                    break;
                case 500:
                    this.message = data.message;
                    break;
                default:
                    throw `${data.code}: ${data.message}`;
            }
        } 
        catch (error) {
            console.error('Error:', error);
            // Handle other errors or display a general error message
        }
    },
    async withdrawWalletTransaction() {
        const jsonData = JSON.stringify({
        SourceWallet: null,
        DestinationWallet: this.destinationwallet.WID,
        CustomerId: this.customer_id,
        WalletTransaction: false,
        ExchangeRate: this.exchange_rate,
        TimeStamp: new Date(),
        AmountTransferred: this.wallet_amount * this.exchange_rate
        });
        const url = create_transaction;
        const postMethod = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonData
        };
    
        try {
            const response = await fetch(url, postMethod);
            const data = await response.json();
    
            switch (data.code) {
                case 201:
                    // Handle success case
                    break;
                case 500:
                    this.message = data.message;
                    break;
                default:
                    throw `${data.code}: ${data.message}`;
            }
        } 
        catch (error) {
            console.error('Error:', error);
            // Handle other errors or display a general error message
        }
    },
    updateDestinationWallets() {
      if (this.sourcewallet) {
          this.availableDestinationWallets = this.customer_wallets.filter(wallet => wallet.WID !== this.sourcewallet.WID);
      } else {
          this.availableDestinationWallets = this.customer_wallets;
      }
    },
    updateSourceWallets() {
        if (this.destinationwallet) {
            this.availableSourceWallets = this.customer_wallets.filter(wallet => wallet.WID !== this.destinationwallet.WID);
        } else {
            this.availableSourceWallets = this.customer_wallets;
        }
    },
    updateAmount(event) {
      // Update the wallet_amount when the input changes
      const value = parseFloat(event.target.value);
      this.wallet_amount = isNaN(value) || value < 0 ? 0.1 : value;
  },
  created() {
    this.get_wallets();
    this.get_transactions();
    this.getCurrencyCodes();
  },
});
const vm = wallet.mount('#wallet');
