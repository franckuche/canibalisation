import streamlit as st
import pandas as pd

st.title("Analyseur de données SEO")

uploaded_file = st.file_uploader("Veuillez envoyer votre fichier CSV", type=['csv'])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, thousands=' ', decimal=',')
    
    # Conversion des colonnes 'Clicks' et 'Impressions' en entiers
    data['Clicks'] = data['Clicks'].str.replace('\u202f', '').astype(int)
    data['Impressions'] = data['Impressions'].str.replace('\u202f', '').astype(int)

    # Conversion de la colonne 'CTR' en décimal, après avoir supprimé le signe '%'
    data['CTR'] = data['CTR'].str.replace('%', '').astype(float) / 100

    # Vérification de l'existence des colonnes requises
    if set(['Query', 'Page', 'Clicks', 'Impressions', 'CTR', 'Position']).issubset(data.columns):

        # Groupement des données par Query et Page
        grouped_data = data.groupby(['Query', 'Page']).agg({'Clicks': 'sum', 'Impressions': 'sum', 'Position': 'mean'}).reset_index()

        # Suppression des mots-clés ayant un match avec une seule page
        counts = grouped_data['Query'].value_counts()
        multiple_pages = counts[counts > 1].index
        filtered_data = grouped_data[grouped_data['Query'].isin(multiple_pages)]

        # Affichage des résultats
        st.write(filtered_data)

        # Téléchargement des résultats
        csv = filtered_data.to_csv(index=False, encoding="utf-8")
        st.download_button(label="Télécharger le CSV", data=csv, file_name="analyse_seo.csv", mime="text/csv")

    else:
        st.error("Le fichier CSV fourni ne contient pas toutes les colonnes nécessaires ('Query', 'Page', 'Clicks', 'Impressions', 'CTR', 'Position')")

else:
    st.warning("Veuillez uploader un fichier CSV.")
