import requests
from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME, GOOGLE_MAPS_API_KEY

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
