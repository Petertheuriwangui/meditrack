from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patientName = db.Column(db.String(150))
    phoneNumber = db.Column(db.String(15))
    note = db.Column(db.String(10000))
    paymentMethod = db.Column(db.String(50))
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    
import base64
import requests
from datetime import datetime

class MpesaSTKPush:
    def __init__(self):
        self.business_shortcode = "174379"
        self.passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        self.consumer_key = "zXJop97aivNrEMehhPL3BreqXLISMv80yk3CjhFPDHIcTF7M"
        self.consumer_secret = "ujq7WcAGNsMkLxoQWg4CY35C2p1rxNDsfV9aFA3JXpjXjYL6lHFOMlFtaxTQ2tXd"
        self.base_url = "https://sandbox.safaricom.co.ke"
  
    def initiate_stk_push(self, phone_number, amount):
        token = self.get_access_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{self.business_shortcode}{self.passkey}{timestamp}".encode()).decode()
    
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
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
            "CallBackURL": "https://mydomain.com/b2b-express-checkout/",
            "AccountReference": "MediTrack",
            "TransactionDesc": "Payment for MediTrack services"
        }
    
        try:
            response = requests.post(
                f"{self.base_url}/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers=headers,
                verify=False
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {"error": "Invalid response from M-Pesa API", "raw_response": response.text}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
    def get_access_token(self):
        auth = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials",
            headers=headers,
            verify=False  # For sandbox testing only
        )
        
        if response.status_code == 200:
            return response.json()['access_token']
        return None
    
    