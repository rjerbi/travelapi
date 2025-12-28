# create_admin.py
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["backend_api_db"]  # Your database name
admins = db.admins

# Admin credentials
email = "admin@gmail.com"
password = "Admin123"

# Hash the password
hashed_password = generate_password_hash(password)

# Insert admin if not already in the database
if not admins.find_one({"email": email}):
    admins.insert_one({
        "email": email,
        "mot_de_passe": hashed_password
    })
    print("Admin created successfully.")
else:
    print("Admin already exists.")
