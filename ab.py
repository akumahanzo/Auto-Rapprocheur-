import pandas as pd
from datetime import datetime
from io import BytesIO


def normalize_date(date):
    """Convertit une date en format YYYY-MM."""
    try:
        if pd.isnull(date):
            return None
        date_obj = pd.to_datetime(date, errors='coerce')
        if pd.isnull(date_obj):
            return None
        return date_obj.strftime('%Y-%m')
    except Exception:
        return None


def traiter_rapprochement(fichier_original, fichier_fournisseur):

    try:

        df_orig = pd.read_excel(fichier_original, dtype=str)
        df_fourn = pd.read_excel(fichier_fournisseur)

        # Normalisation dates
        if 'Date' in df_orig.columns:
            df_orig['Date'] = df_orig['Date'].apply(normalize_date)

        if 'Date' in df_fourn.columns:
            df_fourn['Date'] = df_fourn['Date'].apply(normalize_date)

        # Conversion montants
        df_orig['Total TTC'] = pd.to_numeric(df_orig['Total TTC'], errors='coerce')
        df_fourn['Montant TTC'] = pd.to_numeric(df_fourn['Montant TTC'], errors='coerce')

        # Supprimer factures annulées
        df_fourn = df_fourn[
            ~df_fourn['Annulé'].astype(str).str.upper().str.strip().eq('=VRAI()')
        ]

        df_fourn = df_fourn[
            ~df_fourn['Annulé'].eq(True)
        ]

        resultats = []
        factures_concat_ok = []

        for _, row in df_orig.iterrows():

            facture = row['Facture']
            montant_facture = row['Total TTC']

            mask = df_fourn['N° facture fournisseur'].astype(str).str.contains(
                str(facture),
                na=False
            )

            matching_fourn = df_fourn[mask]

            if not matching_fourn.empty:

                total_fournisseur = matching_fourn['Montant TTC'].sum()

                if abs(total_fournisseur - montant_facture) < 0.01:
                    rapprochement = "OK"
                    difference = 0
                else:
                    rapprochement = "Différent"
                    difference = round(montant_facture - total_fournisseur, 2)

                numeros_concat = " | ".join(
                    matching_fourn['N°'].astype(str)
                ) if 'N°' in matching_fourn.columns else ""

                factures_fournisseur = " | ".join(
                    matching_fourn['N° facture fournisseur'].astype(str)
                )

            else:

                total_fournisseur = 0
                numeros_concat = ""
                rapprochement = "Différent"
                difference = montant_facture
                factures_fournisseur = ""

            if rapprochement == "OK" and numeros_concat:
                factures_concat_ok.append(numeros_concat)

            resultats.append({
                'Facture': facture,
                'Total TTC (original)': montant_facture,
                'Factures fournisseur': factures_fournisseur,
                'N°': numeros_concat,
                'Montant TTC (fournisseur)': total_fournisseur,
                'Rapprochement': rapprochement,
                'Différence': difference
            })

        df_resultat = pd.DataFrame(resultats)

        df_factures = pd.DataFrame({
            'N° Factures OK': [" | ".join(factures_concat_ok)]
        })

        # Création fichier Excel en mémoire
        output = BytesIO()

        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:

            df_resultat.to_excel(
                writer,
                sheet_name='Résultats',
                index=False
            )

            df_factures.to_excel(
                writer,
                sheet_name='Factures Concatenées',
                index=False
            )

        output.seek(0)

        return output

    except Exception as e:
        raise Exception(f"Erreur lors du rapprochement : {e}")
