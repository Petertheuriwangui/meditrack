import requests
from datetime import datetime
import base64
import json

class MpesaSTKPush:
    def __init__(self):
        self.business_shortcode = "174379"  # Lipa Na Mpesa Online Shortcode
        self.passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"  # Your Pass Key
        self.consumer_key = "zXJop97aivNrEMehhPL3BreqXLISMv80yk3CjhFPDHIcTF7M"
        self.consumer_secret = "ujq7WcAGNsMkLxoQWg4CY35C2p1rxNDsfV9aFA3JXpjXjYL6lHFOMlFtaxTQ2tXd"
        self.base_url = "https://sandbox.safaricom.co.ke"  # Change to production URL when going live

    def get_access_token(self):
        auth_url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        auth_string = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth_string}"
        }
        
        response = requests.get(auth_url, headers=headers)
        return response.json()["access_token"]

    def generate_password(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password_str = f"{self.business_shortcode}{self.passkey}{timestamp}"
        return base64.b64encode(password_str.encode()).decode(), timestamp

    def initiate_stk_push(self, phone_number, amount, callback_url, account_reference, transaction_desc):
        access_token = self.get_access_token()
        password, timestamp = self.generate_password()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }
        
        response = requests.post(
            f"{self.base_url}/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers=headers
        )
        
        return response.json()

# Usage Example
if __name__ == "__main__":
    mpesa = MpesaSTKPush()
    
    # Initialize payment
    response = mpesa.initiate_stk_push(
        phone_number="254793548688",  # Format: 254XXXXXXXXX
        amount=1,  # Amount in KES
        callback_url="https://mydomain.com/b2b-express-checkout/",
        account_reference="008401411604",
        transaction_desc="Test Payment"
    )
    
    print(json.dumps(response, indent=2))
