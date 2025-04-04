import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client_id = os.getenv("pVERIFY_CLIENT_ID")
client_secret = os.getenv("pVERIFY_CLIENT_SECRET")


def generate_token():
    url = "https://api.pverify.com/Token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    print(url)
    print(payload)
    print(headers)
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error generating token: {str(e)}")
        return None


if __name__ == "__main__":
    token = generate_token()
    if token:
        print("New token generated:")
        print(token)
