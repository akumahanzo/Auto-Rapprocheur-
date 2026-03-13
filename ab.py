import pandas as pd
from io import BytesIO


def traiter_rapprochement(fichier_releve, fichier_fea):

    # Lecture des fichiers
    df_releve = pd.read_excel(fichier_releve)
    df_fea = pd.read_excel(fichier_fea)

    # Exemple de rapprochement simple (à adapter avec ta logique)
    df_resultat = pd.merge(
        df_releve,
        df_fea,
        how="outer",
        indicator=True
    )

    # Création du fichier Excel en mémoire
    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:

        df_releve.to_excel(writer, sheet_name="Releve", index=False)
        df_fea.to_excel(writer, sheet_name="FAE", index=False)
        df_resultat.to_excel(writer, sheet_name="Rapprochement", index=False)

    output.seek(0)

    return output
