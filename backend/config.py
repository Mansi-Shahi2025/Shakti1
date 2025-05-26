from urllib.parse import quote_plus
# Safely encode MongoDB credentials
username = quote_plus("deep")
password = quote_plus("Thew@rrior23")
cluster_url = "cluster0.1msemag.mongodb.net"

# MongoDB connection string
MONGO_URI = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"

# Replace with your actual database and collection names
DATABASE_NAME = "your_database_name"
COLLECTION_NAME = "your_collection_name"

# Gmail Configuration
GMAIL_ADDRESS = 'lionxyz335@gmail.com'
GMAIL_APP_PASSWORD = 'jfxi zobe hgwe rgmg'

# Emergency Contacts
EMERGENCY_CONTACTS = [
    'chaudharydeepanshu817@gmail.com',
    # Add more if needed
]
GOOGLE_MAPS_API_KEY = "AIzaSyD1OP34CrWgFEK3R-NgERmE0F_HrXnBJbU"