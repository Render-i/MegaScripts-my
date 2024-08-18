import requests
import subprocess
import time
import re
import random
import string
import csv
import threading
import sys
import os

def find_megatools():
    try:
        # Try to find megatools using which
        result = subprocess.run(["which", "megatools"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        # If which fails, try to find megatools manually
        common_paths = [
            "/usr/bin/megatools",
            "/usr/local/bin/megatools",
            "/snap/bin/megatools"
        ]
        for path in common_paths:
            if os.path.exists(path):
                return path
        return None

def install_megatools():
    print("Checking megatools installation...")
    subprocess.run(["apt-get", "update"], check=True)
    subprocess.run(["apt-get", "install", "-y", "megatools"], check=True)
    
    megatools_path = find_megatools()
    if megatools_path:
        print(f"Megatools found at: {megatools_path}")
        return megatools_path
    else:
        raise Exception("Megatools not found after installation. Please install manually and add to PATH.")

# Install megatools and get its path
MEGATOOLS_PATH = install_megatools()

PASSWORD = "examplepassword"  # at least 8 chars

def find_url(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»""'']))"
    url = re.findall(regex, string)
    return [x[0] for x in url]

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

    def verify(self):
        # ... [rest of the code remains the same] ...

def new_account():
    name = "".join(random.choice(string.ascii_letters) for x in range(12))
    acc = MegaAccount(name, PASSWORD)
    acc.register()
    print("Registered. Waiting for verification email...")
    acc.verify()

if __name__ == "__main__":
    # how many accounts to create at once (keep the number under 10)
    num_acc = 5
    for count in range(num_acc):
        t = threading.Thread(target=new_account)
        t.start()
