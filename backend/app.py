from flask import Flask, request, jsonify
from flask_cors import CORS
from route_planner import get_safest_route  # import your core logic
from twilio.rest import Client

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Twilio credentials
TWILIO_ACCOUNT_SID = 'ACc601c3926e7db03a30bb6f2d03865f57'
TWILIO_AUTH_TOKEN = '9ec740c49828a5f2a896156c5a7cd81d'
TWILIO_PHONE_NUMBER = '+15855581717'

# Emergency contacts
EMERGENCY_CONTACTS = [
    '+919999277398'
]

# Send SOS SMS
def send_sos_sms(latitude, longitude):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for contact in EMERGENCY_CONTACTS:
        message = client.messages.create(
            body=f"SOS Alert! Location: https://maps.google.com/?q={latitude},{longitude}",
            from_=TWILIO_PHONE_NUMBER,
            to=contact
        )
        print(f"SOS SMS sent to {contact}: {message.sid}")

# Send SOS Call
def send_sos_call(latitude, longitude):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for contact in EMERGENCY_CONTACTS:
        call = client.calls.create(
            twiml=f'<Response><Say voice="alice" loop="3">Emergency! Emergency! Emergency!</Say></Response>',
            from_=TWILIO_PHONE_NUMBER,
            to=contact
        )
        print(f"SOS Call initiated to {contact}: {call.sid}")

# SOS API Endpoint
@app.route('/send_sos', methods=['POST'])
def send_sos():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    if latitude and longitude:
        send_sos_sms(latitude, longitude)
        send_sos_call(latitude, longitude)
        return jsonify({"message": "SOS alerts (SMS and Call) sent successfully!"}), 200
    else:
        return jsonify({"message": "Invalid coordinates!"}), 400

# Safest Route API Endpoint
@app.route('/safest-route', methods=['POST'])
def safest_route():
    data = request.get_json()
    origin = data.get('origin')
    destination = data.get('destination')

    if not origin or not destination:
        return jsonify({"error": "Origin and destination are required"}), 400

    try:
        route = get_safest_route(origin, destination)
        return jsonify({"route": route})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
