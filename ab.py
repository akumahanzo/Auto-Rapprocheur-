import pandas as pd
from datetime import datetime
from io import BytesIO

def normalize_date(date):
    try:
        if pd.isnull(date):
            return None
        date_obj = pd.to_datetime(date, errors='coerce')
        if pd.isnull(date_obj):
            return None
        return date_obj.strftime('%Y-%m')
    except Exception:
        return None

def find_col(df, name):
    """Trouve une colonne sans tenir compte de la casse."""
    for col in df.columns:
        if col.strip().lower() == name.lower():
            return col
    raise Exception(f"Colonne '{name}' introuvable dans le fichier.")

def traiter_rapprochement(fichier_original, fichier_fournisseur):
    try:
        df_orig = pd.read_excel(fichier_original, dtype=str)
        df_fourn = pd.read_excel(fichier_fournisseur)

        df_orig.columns = df_orig.columns.str.strip()
        df_fourn.columns = df_fourn.columns.str.strip()

        col_facture = find_col(df_orig, "Facture")
        col_total_ttc = find_col(df_orig, "Total TTC")

        col_facture_fourn = find_col(df_fourn, "N° facture fournisseur")
        col_montant_ttc = find_col(df_fourn, "Montant TTC")
        col_annule = find_col(df_fourn, "Annulé")

        col_numero = None
        for c in df_fourn.columns:
            if c.strip().lower() == "n°":
                col_numero = c

        if 'Date' in df_orig.columns:
            df_orig['Date'] = df_orig['Date'].apply(normalize_date)
        if 'Date' in df_fourn.columns:
            df_fourn['Date'] = df_fourn['Date'].apply(normalize_date)

        df_orig[col_total_ttc] = pd.to_numeric(df_orig[col_total_ttc], errors='coerce')
        df_fourn[col_montant_ttc] = pd.to_numeric(df_fourn[col_montant_ttc], errors='coerce')

        df_fourn = df_fourn[
            ~df_fourn[col_annule].astype(str).str.upper().str.strip().eq('=VRAI()')
        ]
        df_fourn = df_fourn[~df_fourn[col_annule].eq(True)]

        resultats = []
        factures_concat_ok = []

        for _, row in df_orig.iterrows():
            facture = row[col_facture]
            montant_facture = row[col_total_ttc]

            mask = df_fourn[col_facture_fourn].astype(str).str.contains(str(facture), na=False)
            matching_fourn = df_fourn[mask]

            if not matching_fourn.empty:
                total_fournisseur = matching_fourn[col_montant_ttc].sum()
                if abs(total_fournisseur - montant_facture) < 0.01:
                    rapprochement = "OK"
                    difference = 0
                else:
                    rapprochement = "Différent"
                    difference = round(montant_facture - total_fournisseur, 2)
                numeros_concat = " | ".join(matching_fourn[col_numero].astype(str)) if col_numero else ""
                factures_fournisseur = " | ".join(matching_fourn[col_facture_fourn].astype(str))
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
        df_factures = pd.DataFrame({'N° Factures OK': [" | ".join(factures_concat_ok)]})

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_resultat.to_excel(writer, sheet_name='Résultats', index=False)
            df_factures.to_excel(writer, sheet_name='Factures Concatenées', index=False)
        output.seek(0)

        return output

    except Exception as e:
        raise Exception(f"Erreur lors du rapprochement : {e}")
