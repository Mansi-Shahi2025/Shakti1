from flask import Flask, request
from twilio.rest import Client
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Twilio credentials
TWILIO_ACCOUNT_SID = 'ACc601c3926e7db03a30bb6f2d03865f57'
TWILIO_AUTH_TOKEN = '9ec740c49828a5f2a896156c5a7cd81d'
TWILIO_PHONE_NUMBER = '+12316266151'

# Emergency contacts list
EMERGENCY_CONTACTS = [
    #'+919711590362',
    '+919999277398'
]

def send_sos_sms(latitude, longitude):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for contact in EMERGENCY_CONTACTS:
        message = client.messages.create(
            body=f"SOS Alert! Location: https://maps.google.com/?q={latitude},{longitude}",
            from_=TWILIO_PHONE_NUMBER,
            to=contact
        )
        print(f"SOS sent to {contact}: {message.sid}")

@app.route('/send_sos', methods=['POST'])
def send_sos():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    if latitude and longitude:
        send_sos_sms(latitude, longitude)
        return {"message": "SOS alerts sent successfully!"}, 200
    else:
        return {"message": "Invalid coordinates!"}, 400

if __name__ == '__main__':
    app.run(debug=True)