import streamlit as st
from auth import login
from rapprochement import app_rapprochement

st.set_page_config(page_title="ISS Solutions")

st.title("ISS Solutions")

# Init session
if "auth" not in st.session_state:
    st.session_state["auth"] = False

# 🔐 Si pas connecté → écran login uniquement
if not st.session_state["auth"]:
    st.header("Connexion")

    username = st.text_input("Nom utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Login"):
        if login(username, password):
            st.session_state["auth"] = True
            st.rerun()
        else:
            st.error("Login incorrect.")

# ✅ Si connecté → app
else:
    st.sidebar.success("Connecté")

    if st.sidebar.button("Logout"):
        st.session_state["auth"] = False
        st.rerun()

    app_rapprochement()
