import requests
from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME, GOOGLE_MAPS_API_KEY
from flask import Flask, request
from twilio.rest import Client
from flask_cors import CORS

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
crime_collection = db[COLLECTION_NAME]

GOOGLE_MAPS_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"

def get_google_maps_route(origin, destination):
    params = {
        "origin": origin,
        "destination": destination,
        "key": GOOGLE_MAPS_API_KEY,
        "mode": "driving",
    }
    response = requests.get(GOOGLE_MAPS_DIRECTIONS_URL, params=params)
    response.raise_for_status()
    data = response.json()

    if data["status"] != "OK":
        raise Exception(f"Google Maps API error: {data['status']}")

    route_points = []
    for leg in data["routes"][0]["legs"]:
        for step in leg["steps"]:
            start_loc = step["start_location"]
            route_points.append((start_loc["lat"], start_loc["lng"]))
        # Append last step end location
        end_loc = leg["steps"][-1]["end_location"]
        route_points.append((end_loc["lat"], end_loc["lng"]))

    return route_points

def calculate_safety_score_for_point(lat, lng):
    # Example MongoDB geo-query placeholder: find nearest city and get its safety_score
    city = crime_collection.find_one({"location_key": "some_city_key"})  # Replace with geoquery!
    if city and "safety_score" in city:
        return city["safety_score"]
    return float('inf')  # very unsafe if unknown

def filter_safest_route(route_points):
    # TODO: Implement actual filtering logic based on safety scores per point
    # For now, just return the original route as is
    return route_points

def get_safest_route(origin, destination):
    # Get route points from Google Directions API
    route_points = get_google_maps_route(origin, destination)

    # Filter or reorder the route based on safety data
    safest_route_points = filter_safest_route(route_points)

    # Convert to list of lists (instead of tuples) for JSON serialization
    route = [[lat, lng] for lat, lng in safest_route_points]
    return route


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Twilio credentials
TWILIO_ACCOUNT_SID = 'ACc601c3926e7db03a30bb6f2d03865f57'
TWILIO_AUTH_TOKEN = '9ec740c49828a5f2a896156c5a7cd81d'
TWILIO_PHONE_NUMBER = '+15855581717'  # Must support both SMS and Voice

# Emergency contacts list
EMERGENCY_CONTACTS = [
    # Add more verified numbers if you're on a trial account
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

# Send SOS voice call
def send_sos_call(latitude, longitude):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for contact in EMERGENCY_CONTACTS:
        call = client.calls.create(
            twiml=f'<Response><Say voice="alice" loop="3">Emergency! Emergency! Emergency!</Say></Response>',
            from_=TWILIO_PHONE_NUMBER,
            to=contact
        )
        print(f"SOS Call initiated to {contact}: {call.sid}")


# API endpoint to send SOS alerts
@app.route('/send_sos', methods=['POST'])
def send_sos():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    if latitude and longitude:
        send_sos_sms(latitude, longitude)
        send_sos_call(latitude, longitude)
        return {"message": "SOS alerts (SMS and Call) sent successfully!"}, 200
    else:
        return {"message": "Invalid coordinates!"}, 400

if __name__ == '__main__':
    app.run(debug=True)