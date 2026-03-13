import json
import hashlib
import smtplib
from email.mime.text import MIMEText
from pathlib import Path

BASE = Path("admin_data")

users_file = BASE / "users.json"
keys_file = BASE / "activation_keys.json"
config_file = BASE / "config.json"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_json(path):
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def send_request_email(email, organisation, nom, solution):
    """Envoie un email aux admins avec la demande de création de compte"""
    config = load_json(config_file)
    admins = config["admin_emails"]

    body = f"""
Nouvelle demande de compte ISS

Nom: {nom}
Email: {email}
Organisation: {organisation}
Solution: {solution}
"""

    msg = MIMEText(body)
    msg["Subject"] = "Demande de compte ISS"
    msg["From"] = email

    # ⚠️ Configurer avec ton compte Gmail et App Password
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("ton_email@gmail.com", "app_password")  # à remplacer

    for admin in admins:
        msg["To"] = admin
        server.sendmail(email, admin, msg.as_string())

    server.quit()


def activate_account(username, password, key):
    """Active un compte si la clé d'activation est valide"""
    users = load_json(users_file)
    keys = load_json(keys_file)

    for k in keys.get("keys", []):
        if k["username"] == username and k["activation_key"] == key and not k["used"]:
            users.setdefault("users", []).append({
                "username": username,
                "password": hash_password(password)
            })
            k["used"] = True
            save_json(users_file, users)
            save_json(keys_file, keys)
            return True
    return False


def login(username, password):
    """Vérifie si le login est correct"""
    users = load_json(users_file)
    hashed = hash_password(password)
    for u in users.get("users", []):
        if u["username"] == username and u["password"] == hashed:
            return True
    return False
