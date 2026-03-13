import streamlit as st
from auth import login, activate_account, send_request_email
from rapprochement import app_rapprochement

st.set_page_config(page_title="ISS Solutions")

st.title("ISS Solutions")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Créer demande compte", "Activer compte"]
)

if menu == "Créer demande compte":
    st.header("Demande de compte")
    nom = st.text_input("Nom complet")
    email = st.text_input("Email")
    organisation = st.text_input("Organisation")
    solution = st.text_input("Solution / application")
    if st.button("Envoyer demande"):
        send_request_email(email, organisation, nom, solution)
        st.success("Demande envoyée aux administrateurs.")

elif menu == "Activer compte":
    st.header("Activation")
    username = st.text_input("Nom utilisateur")
    password = st.text_input("Mot de passe", type="password")
    key = st.text_input("Clé activation")
    if st.button("Activer"):
        if activate_account(username, password, key):
            st.success("Compte activé ! Vous pouvez maintenant vous connecter.")
        else:
            st.error("Clé invalide ou déjà utilisée.")

elif menu == "Login":
    st.header("Connexion")
    username = st.text_input("Nom utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Login"):
        if login(username, password):
            st.session_state["auth"] = True
        else:
            st.error("Login incorrect.")

if st.session_state["auth"]:
    st.sidebar.success("Connecté")
    app_rapprochement()
