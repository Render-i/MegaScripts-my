import requests
import subprocess
import time
import re
import random
import string
import csv
import threading

# Install megatools
!apt-get update
!apt-get install -y megatools

# Find the path to megatools
MEGATOOLS_PATH = !which megatools
MEGATOOLS_PATH = MEGATOOLS_PATH[0].strip()

PASSWORD = "examplepassword"  # at least 8 chars

# ... [previous code remains the same] ...

class MegaAccount:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def register(self):
        mail_req = requests.get(
            "https://api.guerrillamail.com/ajax.php?f=get_email_address&lang=en"
        ).json()
        self.email = mail_req["email_addr"]
        self.email_token = mail_req["sid_token"]

        # begin registration
        registration = subprocess.run(
            [
                MEGATOOLS_PATH,
                "reg",
                "--scripted",
                "--register",
                "--email",
                self.email,
                "--name",
                self.name,
                "--password",
                self.password,
            ],
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.verify_command = registration.stdout

    # ... [rest of the code remains the same] ...

if __name__ == "__main__":
    # how many accounts to create at once (keep the number under 10)
    num_acc = 5
    for count in range(num_acc):
        t = threading.Thread(target=new_account)
        t.start()
