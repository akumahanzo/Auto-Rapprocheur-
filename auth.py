# auth.py
import json
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Fichier admin pour stocker les adresses qui recevront les demandes
ADMIN_FILE = "admin_data.json"  # contient une liste d'emails admins
USERS_FILE = "users_data.json"  # stockage des comptes activés

# ----------------------
# Gestion des emails
# ----------------------
EMAIL_USER = "mail_essai@mail.com"  # Email pour envoyer les demandes
EMAIL_PASS = "mdp123"                # Mot de passe d'exemple

def send_request_email(user_email, organisation, nom, solution):
    """Envoie un email de demande de création de compte aux admins."""
    # Charger les adresses admins depuis le fichier JSON
    try:
        with open(ADMIN_FILE, "r") as f:
            admins = json.load(f)
    except FileNotFoundError:
        admins = ["mo.cherdoudi@gmail.com"]  # fallback par défaut

    subject = "Nouvelle demande de compte ISS"
    body = f"""
Bonjour Admin,

Un utilisateur souhaite créer un compte ISS :

Nom complet : {nom}
Email : {user_email}
Organisation : {organisation}
Solution / Application : {solution}

Veuillez traiter cette demande et générer un compte.
"""

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = ", ".join(admins)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, admins, msg.as_string())
        server.quit()
        print("Email envoyé aux admins :", admins)
    except Exception as e:
        print("Erreur lors de l'envoi de l'email :", e)


# ----------------------
# Gestion des comptes
# ----------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def activate_account(username, password, key):
    """Active un compte si la clé correspond à celle générée par l'admin"""
    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}

    if username in users and users[username].get("active", False):
        return False  # déjà activé

    # Exemple simple : clé d'activation fixe pour test
    if key == "CLE12345":
        users[username] = {
            "password": hash_password(password),
            "key": key,
            "active": True
        }
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
        return True
    return False


def login(username, password):
    """Vérifie login / mot de passe"""
    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        return False

    if username in users and users[username].get("active", False):
        return hash_password(password) == users[username]["password"]
    return False
