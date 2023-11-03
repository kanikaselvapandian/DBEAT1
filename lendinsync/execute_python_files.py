import subprocess
import signal
import os

# List of Python files we need to run (app.py, services)
flask_apps = {"app.py":5000, 
                "transfer_management_service/wallet.py":7000, 
                "transfer_management_service/transaction.py":8000, 
                "transfer_management_service/friend.py":8895, 
                "transfer_management_service/transfer_management.py":6100, 
                "loans_service/loan.py":5001,
                } 

# Dictionary to hold references to subprocesses
processes = {}

def run_flask_apps(apps):
    for file, port in apps.items():
        print(f"Running {file} on port {port}...")
        command = f"python {file} --port {port}"  # Assuming Flask apps accept a '--port' argument
        process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
        processes[file] = process  # Store reference to subprocess
        print(f"Started {file} on port {port} with PID {process.pid}")

def stop_flask_apps():
    for file, process in processes.items():
        print(f"Stopping {file}...")
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)  # Terminate the subprocess group

if __name__ == "__main__":
    try:
        run_flask_apps(flask_apps)
        # Allow the script to continue running, waiting for Ctrl + C to stop the processes
        while True:
            pass
    except KeyboardInterrupt:
        print("\nStopping Flask applications...")
        stop_flask_apps()
