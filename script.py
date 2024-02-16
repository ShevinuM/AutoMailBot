from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
from pymongo import MongoClient
import getpass
from email_validator import validate_email, EmailNotValidError
import smtplib

client = MongoClient('mongodb://localhost:27017/')
db = client['Researchers']
coll = db['Test']

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

EMAIL_USER, PASS = None, None
while True:
    try:
        EMAIL_USER = input("Please enter you email: ")
        break
    except:
        print("Email is not valid")

while True:
    try:
        PASS = getpass.getpass() 
        server.login(EMAIL_USER, PASS)
        break
    except Exception as e:
        print("Invalid email or password")
        print("Error", str(e))

data = coll.find({}, {'last_name': 1,
                      'email': 1,})


for item in data:
    email = item['email']
    last_name = item['last_name']

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg['Subject'] = "This is a test"

    with open('message.html', 'r') as f:
        html = f.read()

    html = html.format(last_name=last_name)

    msg.attach(MIMEText(html, 'html'))
    server.sendmail(EMAIL_USER, email, msg.as_string())