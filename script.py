from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
from pymongo import MongoClient
import getpass
from email_validator import validate_email, EmailNotValidError
import smtplib
from dotenv import load_dotenv
import os


load_dotenv()

client = MongoClient('mongodb://localhost:27017/')
db = client['Researchers']
coll = db['NotOnYaffle']

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

PASS = None

EMAIL_USER = os.getenv('USER_MAIL') 

while True:
    try:
        PASS = os.getenv("PASS") 
        server.login(EMAIL_USER, PASS)
        break
    except Exception as e:
        print("Invalid email or password")
        sys.exit()

data = coll.find({}, {'first_name': 1,
                      'last_name': 1,
                      'email': 1,})


for item in data:
    email = item['email']
    first_name = item['first_name']
    last_name = item['last_name']

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg['Subject'] = "Cold Ocean & Northern activities and Yaffle"

    with open('message.html', 'r') as f:
        html = f.read()

    html = html.format(last_name=last_name)

    msg.attach(MIMEText(html, 'html'))
    try:
        server.sendmail(EMAIL_USER, email, msg.as_string())
        with open("sent_emails.txt", 'a') as f:
            f.write(f"email: {email:<40}| name: {first_name} {last_name}\n")
    except:
        with open("invalid_emails.txt", 'a') as f:
            f.write(f"email: {email:<40}| name: {first_name} {last_name}\n")

