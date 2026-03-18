import json

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)["users"]

def login(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True
    return False
