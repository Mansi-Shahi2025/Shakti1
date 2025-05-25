from flask import Flask, request, jsonify
from flask_cors import CORS
from sos import send_sos_alert
from route_planner import get_safest_route  # import the core function

app = Flask(__name__)
CORS(app)

@app.route('/send_sos', methods=['POST'])
def send_sos():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude and longitude:
        send_sos_alert(latitude, longitude)
        return {"message": "SOS alerts sent successfully!"}, 200
    else:
        return {"message": "Invalid coordinates!"}, 400

@app.route('/safest-route', methods=['POST'])
def safest_route():
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')

    if not origin or not destination:
        return jsonify({"error": "Origin and destination are required"}), 400

    try:
        route = get_safest_route(origin, destination)
        return jsonify({"route": route})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
