# delete_admin.py
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["backend_api_db"]  # Your database name
admins = db.admins

# Admin email to delete
email_to_delete = "admin@example.com"

# Delete admin by email
result = admins.delete_one({"email": email_to_delete})

if result.deleted_count > 0:
    print("Admin deleted successfully.")
else:
    print("Admin not found.")
