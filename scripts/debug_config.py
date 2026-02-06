import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.config import settings

print(f"CWD: {os.getcwd()}")
print(f"Env file path: {os.path.abspath('.env')}")
print(f"Env file exists: {os.path.exists('.env')}")

# Read raw .env to see if it's there
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        print("--- .env content (obscured) ---")
        for line in f:
            if "PASSWORD" in line:
                print("SMTP_PASSWORD=******")
            else:
                print(line.strip())
    print("-------------------------------")

print(f"Settings Loaded:")
print(f"SMTP_USERNAME: {settings.SMTP_USERNAME}")
print(f"SMTP_SERVER: {settings.SMTP_SERVER}")

if settings.SMTP_USERNAME:
    print("SUCCESS: Credentials loaded.")
else:
    print("FAILURE: Credentials returned None.")
