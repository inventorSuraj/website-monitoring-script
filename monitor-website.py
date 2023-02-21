import time
import webbrowser
import requests
import os
from datetime import datetime, timedelta
import sys
import subprocess
import urllib.request

# Check if Python is installed
try:
    version = subprocess.check_output(["python", "--version"])
    print("Python is already installed.")
except:
    print("Python is not installed. Downloading and installing Python...")
    # Download and install the latest version of Python
    if sys.platform == 'win32':
        # Windows
        url = "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe"
        filename = "python.exe"
        urllib.request.urlretrieve(url, filename)
        subprocess.call([filename, "/quiet", "InstallAllUsers=1", "PrependPath=1"])
    else:
        # macOS or Linux
        url = "https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz"
        filename = "Python-3.10.0.tgz"
        urllib.request.urlretrieve(url, filename)
        subprocess.call(["tar", "-xzf", filename])
        os.chdir("Python-3.10.0")
        subprocess.call(["./configure"])
        subprocess.call(["make"])
        subprocess.call(["make", "install"])
    print("Python has been installed.")

    # Restart the script with the newly installed Python
    os.execv(sys.executable, [sys.executable] + sys.argv)

# If we get here, Python is installed
url = input("Enter the URL of the website you want to monitor: ")
interval = input("Enter the time interval in seconds (e.g. 60 for every minute): ")
start_date_str = input("Enter the start date in yyyy-mm-dd format: ")
end_date_str = input("Enter the end date in yyyy-mm-dd format: ")

start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

while datetime.now() < start_date:
    time.sleep(1)

while datetime.now() <= end_date:
    response = requests.get(url)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if response.status_code != 200:
        print(f"[{current_time}] ERROR: Could not connect to {url}.")
    else:
        if "last_response" not in locals():
            last_response = response.text
        else:
            if response.text != last_response:
                print(f"[{current_time}] CHANGE DETECTED: {url}")
                webbrowser.open(url)
                break
            else:
                print(f"[{current_time}] No change detected.")
        last_response = response.text

    time.sleep(int(interval))

print("Monitoring has ended.")
