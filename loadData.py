import sys
from email_validator import validate_email
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from docx import Document

with open('excluded.txt', 'w') as f:
    pass
with open('noEmail.txt', 'w') as f:
    pass
with open('duplicates.txt', 'w') as f:
    pass

client = MongoClient('mongodb://localhost:27017/')
db = client['Researchers']
coll = db['NotOnYaffle']

coll.drop()

coll = db['NotOnYaffle']
coll.create_index("email", unique=True)

doc = Document('researchers.docx')
table = doc.tables[0]

toExclude = set()
with open('exclude.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        toExclude.add(line)

toInsert = []
for row in table.rows[1:]:
    name = row.cells[0].text.strip()
    email = row.cells[1].text.strip()
    print(email)
    if name == "" and email == "":
        continue
    if email in toExclude:
        with open('excluded.txt', 'a') as te:
            te.write(f"name: {name:<30}| email: {email}\n")
    if email == "-":
        with open('noEmail.txt', 'a') as ne:
            ne.write(f"{name}\n")
        continue
    split_name = name.rsplit(' ', 1)
    if len(split_name) < 2:
        raise ValueError("Invalid entry")
    first_name, last_name = split_name[0], split_name[-1]
    try:
        v = validate_email(email)
    except:
        raise ValueError("Invalid Email")
    try:
        coll.insert_one({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        })
    except DuplicateKeyError:
        with open('duplicates.txt', 'a') as f:
            f.write(f"{name}, {email}\n")