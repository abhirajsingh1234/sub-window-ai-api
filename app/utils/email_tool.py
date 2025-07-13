import smtplib
from email.mime.text import MIMEText
import os
import dotenv

def send_emails(recipient, subject, body):
    
    dotenv.load_dotenv()
    smtp_server = "smtp.gmail.com"
    port = 587  # TLS port
    sender_email = "rajpurohitabhirajsingh@gmail.com"         # Replace with your email
    password = os.getenv("MAIL_ID_PASSWORD")                  # Replace with your app password (if using Gmail, set up 2FA and generate an app password)
    receiver_email = recipient
    subject = subject
    body = body
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()           
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    return f"email was sent by {sender_email} to {receiver_email} and  subject was {subject}, body was {body}"

