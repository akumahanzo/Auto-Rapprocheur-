import pandas as pd
from io import BytesIO


def traiter_rapprochement(fichier_releve, fichier_fea):

    try:

        # lecture fichiers
        df_releve = pd.read_excel(fichier_releve)
        df_fea = pd.read_excel(fichier_fea)

    except Exception as e:
        raise Exception(f"Erreur lors de la lecture des fichiers Excel : {e}")

    try:

        # ------------------------------
        # ICI TU METS TON ALGORITHME
        # EXACTEMENT COMME AVANT
        # ------------------------------

        df_resultat = df_releve.copy()

        # Exemple placeholder
        df_resultat["Source"] = "Relevé"

    except Exception as e:
        raise Exception(f"Erreur pendant le rapprochement : {e}")

    try:

        output = BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:

            df_resultat.to_excel(
                writer,
                sheet_name="Rapprochement",
                index=False
            )

        output.seek(0)

        return output

    except Exception as e:
        raise Exception(f"Erreur lors de la génération du rapport Excel : {e}")
