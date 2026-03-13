import streamlit as st
from ab import traiter_rapprochement

st.set_page_config(
    page_title="Assistant Lettrage - ISS",
    layout="centered"
)

st.title("Assistant Lettrage - ISS")

st.write("""
Importer les fichiers nécessaires pour lancer le rapprochement :

1️⃣ Relevé fournisseur Air Sea Maroc  
2️⃣ F.A.E exporté de Business Central
""")

st.divider()

releve_file = st.file_uploader(
    "📂 Importer le relevé fournisseur",
    type=["xlsx"]
)

fea_file = st.file_uploader(
    "📂 Importer le fichier F.A.E (BC)",
    type=["xlsx"]
)

st.divider()

if st.button("🚀 Lancer le rapprochement"):

    if releve_file is None:
        st.error("❌ Veuillez importer le relevé fournisseur.")
        st.stop()

    if fea_file is None:
        st.error("❌ Veuillez importer le fichier F.A.E.")
        st.stop()

    try:

        with st.spinner("⏳ Traitement en cours..."):

            rapport = traiter_rapprochement(fea_file, releve_file)

        st.success("✅ Rapprochement terminé.")

        st.download_button(
            label="📥 Télécharger le rapport Excel",
            data=rapport,
            file_name="rapport_prelettrage.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:

        st.error("❌ Une erreur est survenue pendant le traitement.")
        st.code(str(e))
