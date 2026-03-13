import streamlit as st
from ab import traiter_rapprochement

st.set_page_config(
    page_title="Assistant Lettrage - ISS",
    layout="centered"
)

st.title("Assistant Lettrage - ISS")
st.write("Importer les fichiers nécessaires pour lancer le rapprochement.")

st.divider()

# Upload fichiers
releve_file = st.file_uploader(
    "📂 Importer le relevé du transitaire (Air Sea Maroc)",
    type=["xlsx"]
)

fea_file = st.file_uploader(
    "📂 Importer le F.A.E exporté de BC",
    type=["xlsx"]
)

st.divider()

if st.button("🚀 Lancer le rapprochement"):

    if releve_file is None or fea_file is None:
        st.error("Veuillez importer les deux fichiers.")
    else:

        with st.spinner("Traitement en cours..."):

            rapport = traiter_rapprochement(releve_file, fea_file)

        st.success("Rapprochement terminé.")

        st.download_button(
            label="📥 Télécharger le rapport Excel",
            data=rapport,
            file_name="rapport_rapprochement.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
