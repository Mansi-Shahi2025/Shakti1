from flask import Flask, request
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Your Gmail credentials (use App Password if 2FA is enabled)
GMAIL_ADDRESS = 'lionxyz335@gmail.com'
GMAIL_APP_PASSWORD = 'jfxi zobe hgwe rgmg'  # Get it from https://myaccount.google.com/apppasswords

# List of emergency contact email addresses
EMERGENCY_CONTACTS = [
    'chaudharydeepanshu817@gmail.com',
    # 'emergency2@example.com'
]

def send_sos_email(latitude, longitude, recipient_email):
    # Email body
    message_body = f"SOS Alert!\nLocation: https://maps.google.com/?q={latitude},{longitude}"
    msg = MIMEText(message_body)
    msg['Subject'] = 'SOS Alert'
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = recipient_email

    # Send email using Gmail SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print(f"SOS email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send SOS email to {recipient_email}: {e}")

def send_sos_alert(latitude, longitude):
    for email in EMERGENCY_CONTACTS:
        send_sos_email(latitude, longitude, email)

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

if __name__ == '__main__':
    app.run(debug=True)
