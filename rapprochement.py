# rapprochement.py
import streamlit as st

def app_rapprochement():
    import ab  # import local pour éviter le circular import

    st.set_page_config(page_title="Assistant Lettrage", layout="centered")

    st.title("Assistant Lettrage")
    st.write("Importer les deux fichiers Excel pour lancer le rapprochement.")

    releve_file = st.file_uploader(
        "Relevé fournisseur (contient la colonne Total TTC)",
        type=["xlsx"]
    )

    fae_file = st.file_uploader(
        "Fichier FAE Business Central (contient la colonne Montant TTC)",
        type=["xlsx"]
    )

    if st.button("Lancer le rapprochement"):
        if releve_file is None:
            st.error("Veuillez importer le relevé fournisseur.")
            st.stop()
        if fae_file is None:
            st.error("Veuillez importer le fichier FAE.")
            st.stop()

        try:
            with st.spinner("Traitement en cours..."):
                # Appel de la fonction traiter_rapprochement du module ab
                rapport = ab.traiter_rapprochement(releve_file, fae_file)

            st.success("Rapprochement terminé.")

            st.download_button(
                label="Télécharger le rapport Excel",
                data=rapport,
                file_name="rapport_prelettrage.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(str(e))
