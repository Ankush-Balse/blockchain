import pyrebase
from dotenv import load_dotenv
import os
import json

load_dotenv()

print("Loading Firebase configuration...")
print(f"API Key available: {'Yes' if os.getenv('FIREBASE_API_KEY') else 'No'}")
print(f"Auth Domain: {os.getenv('FIREBASE_AUTH_DOMAIN')}")

# Set a default database URL 
database_url = os.getenv("FIREBASE_DATABASE_URL")
if not database_url:
    project_id = os.getenv("FIREBASE_PROJECT_ID")
    database_url = f"https://{project_id}.firebaseio.com"
    print(f"Database URL was empty, using: {database_url}")

config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": database_url,
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
}

try:
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    print("Firebase initialized successfully")
except Exception as e:
    print(f"Firebase initialization error: {e}")

def register(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print(f"Registration successful for: {email}")
        return "success"
    except Exception as e:
        error_message = str(e)
        print(f"Registration error: {error_message}")
        return error_message  

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(f"Login successful for: {email}")
        return "success"
    except Exception as e:
        error_message = str(e)
        print(f"Login error: {error_message}")
        return error_message  