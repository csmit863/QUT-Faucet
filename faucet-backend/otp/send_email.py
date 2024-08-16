import os, dotenv, smtplib, ssl
from email.mime.text import MIMEText

dotenv.load_dotenv()

def send_email(to_email, message, subject):
    sender_email = os.environ.get('sender_email')
    password = os.environ.get('qutbtc_app_pw')
    smtp_server = "smtp.gmail.com"
    port = 465  
    # Create a secure SSL context
    context = ssl.create_default_context()
    message = MIMEText(message)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = to_email
    # Try to log in to server and send email
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, message.as_string())
