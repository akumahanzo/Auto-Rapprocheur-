import streamlit as st
import pandas as pd
import tempfile
import os
from ab import traiter_rapprochement

st.set_page_config(
    page_title="Assistant Lettrage - ISS",
    layout="centered"
)

st.title("Assistant Lettrage - ISS")
st.write("### Importer les fichiers nécessaires")

# Upload fichiers
releve_file = st.file_uploader(
    "Importer le relevé du transitaire",
    type=["xlsx"]
)

fea_file = st.file_uploader(
    "Importer F.A.E exporté de BC",
    type=["xlsx"]
)

if st.button("Lancer le rapprochement"):

    if releve_file is None or fea_file is None:
        st.error("Veuillez importer les deux fichiers.")
    else:

        with st.spinner("Traitement en cours..."):

            # Sauvegarder temporairement
            temp_dir = tempfile.mkdtemp()

            path_releve = os.path.join(temp_dir, releve_file.name)
            path_fea = os.path.join(temp_dir, fea_file.name)

            with open(path_releve, "wb") as f:
                f.write(releve_file.getbuffer())

            with open(path_fea, "wb") as f:
                f.write(fea_file.getbuffer())

            # Lancer ton script existant
            rapport = traiter_rapprochement(path_releve, path_fea)

        st.success("Rapprochement terminé")

        # proposer téléchargement
        if rapport and os.path.exists(rapport):

            with open(rapport, "rb") as f:
                st.download_button(
                    label="Télécharger le rapport",
                    data=f,
                    file_name="rapport_rapprochement.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
