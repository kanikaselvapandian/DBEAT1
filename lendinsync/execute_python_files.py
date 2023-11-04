import platform
import subprocess
import os
import time

# Define your Flask services and their respective ports
flask_processes = []

flask_services = {
    "app.py": 5000, 
    "transfer_management_service/wallet.py": 7000, 
    "transfer_management_service/transaction.py": 8000, 
    "transfer_management_service/friend.py": 8895, 
    "transfer_management_service/transfer_management.py": 6100, 
    "loans_service/loan.py": 5001,
}

# Function to run Flask services
def run_flask_services():
    current_os = platform.system()

    def start_process(command):
        if current_os == "Windows":
            subprocess.Popen(f"start cmd /k python {command}", shell=True)
        elif current_os == "Darwin":  # macOS
            subprocess.Popen(["python", command])
        else:
            print("Unsupported operating system")
            return None

    try:
        for service, port in flask_services.items():
            command = service
            process = start_process(command)
            if process:
                flask_processes.append(process)
                # Give some time for the server to start before moving on to the next service
                time.sleep(2)
    except KeyboardInterrupt:
        print("Stopping Flask services...")

if __name__ == "__main__":
    run_flask_services()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for process in flask_processes:
            process.terminate()
        print("Flask services stopped.")
