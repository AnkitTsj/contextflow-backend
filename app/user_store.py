import json
import os
from passlib.context import CryptContext

USER_DATA_FILE = "storage/users.json"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _ensure_file_exists():
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
    if not os.path.isfile(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w") as f:
            json.dump({}, f)

def get_all_users():
    _ensure_file_exists()
    with open(USER_DATA_FILE, "r") as f:
        return json.load(f)

def save_all_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

def user_exists(username):
    users = get_all_users()
    return username in users

def create_user(username, password):
    users = get_all_users()
    if username in users:
        return False
    hashed = pwd_context.hash(password)
    users[username] = {
        "username": username,
        "hashed_password": hashed
    }
    save_all_users(users)
    return True

def get_user(username):
    users = get_all_users()
    return users.get(username)
