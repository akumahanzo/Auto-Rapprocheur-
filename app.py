import streamlit as st
from ab import traiter_rapprochement

st.set_page_config(
    page_title="Assistant Lettrage - ISS",
    layout="centered"
)

st.title("Assistant Lettrage - ISS")

st.write("""
Importer les deux fichiers Excel nécessaires pour lancer le rapprochement.

1️⃣ Relevé du transitaire (Air Sea Maroc)  
2️⃣ F.A.E exporté de Business Central  
""")

st.divider()

releve_file = st.file_uploader(
    "📂 Importer le relevé du transitaire",
    type=["xlsx"]
)

fea_file = st.file_uploader(
    "📂 Importer le fichier F.A.E exporté de BC",
    type=["xlsx"]
)

st.divider()

if st.button("🚀 Lancer le rapprochement"):

    if releve_file is None:
        st.error("❌ Aucun relevé du transitaire n'a été importé.")
        st.stop()

    if fea_file is None:
        st.error("❌ Aucun fichier F.A.E n'a été importé.")
        st.stop()

    try:

        with st.spinner("⏳ Traitement en cours..."):

            rapport = traiter_rapprochement(releve_file, fea_file)

        if rapport is None:
            st.error("❌ Le traitement n'a retourné aucun résultat.")
            st.stop()

        st.success("✅ Rapprochement terminé avec succès.")

        st.download_button(
            label="📥 Télécharger le rapport Excel",
            data=rapport,
            file_name="rapport_rapprochement.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:

        st.error("❌ Une erreur est survenue pendant le traitement.")

        st.code(str(e))

        st.warning("""
Vérifiez les points suivants :

• Les deux fichiers sont bien au format Excel (.xlsx)  
• Les colonnes attendues existent dans les fichiers  
• Le relevé Air Sea Maroc est bien nettoyé  
• Le fichier F.A.E provient bien de Business Central
""")
