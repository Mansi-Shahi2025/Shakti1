import smtplib
from email.mime.text import MIMEText
from config import GMAIL_ADDRESS, GMAIL_APP_PASSWORD, EMERGENCY_CONTACTS

def send_sos_email(latitude, longitude, recipient_email):
    message_body = f"SOS Alert!\nLocation: https://maps.google.com/?q={latitude},{longitude}"
    msg = MIMEText(message_body)
    msg['Subject'] = 'SOS Alert'
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = recipient_email

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
