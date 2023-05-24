import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

@st.cache(allow_output_mutation=True)
def load_data(uploaded_file):
    data = pd.read_csv(uploaded_file, thousands=' ', decimal=',')
    data['Clicks'] = data['Clicks'].str.replace('\u202f', '').astype(int)
    data['Impressions'] = data['Impressions'].str.replace('\u202f', '').astype(int)
    data['CTR'] = pd.to_numeric(data['CTR'].str.replace('%', ''), errors='coerce') / 100
    data['Lang'] = np.where(data['Page'].str.contains("/fr/"), "FR",
                   np.where(data['Page'].str.contains("/en/"), "EN", "Unknown"))
    return data

st.title("Analyse de la canibalisation des mots-clés")

uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")
if uploaded_file is not None:
    data = load_data(uploaded_file)
    st.write(data.columns)  # Affichage des colonnes
    st.subheader("Nombre de pages par langue")
    fig, ax = plt.subplots()
    data['Lang'].value_counts().plot(kind='bar', ax=ax)
    st.pyplot(fig)
    
    # Afficher le tableau de données
    st.write(data)

    # Créer des graphiques pour les mots-clés étrangers qui rankent avec des pages FR et EN
    foreign_keywords_fr = data[(data['Lang'] == 'FR') & (data['Query'].str.contains('[a-zA-Z]'))]
    foreign_keywords_en = data[(data['Lang'] == 'EN') & (data['Query'].str.contains('[a-zA-Z]'))]

    # Création des graphiques
    fig, ax = plt.subplots(2, 1, figsize=(10, 10))

    ax[0].bar(foreign_keywords_fr['Query'], foreign_keywords_fr['Impressions'])
    ax[0].set_title('Impressions des mots-clés étrangers sur les pages FR')
    ax[0].set_xticklabels(foreign_keywords_fr['Query'], rotation=90)

    ax[1].bar(foreign_keywords_en['Query'], foreign_keywords_en['Impressions'])
    ax[1].set_title('Impressions des mots-clés étrangers sur les pages EN')
    ax[1].set_xticklabels(foreign_keywords_en['Query'], rotation=90)

    plt.tight_layout()
    st.pyplot(fig)

    # Affichage des URLs avec "/en/" qui ont au moins une impression
    st.subheader("URLs avec '/en/' ayant au moins une impression")
    urls_en = data[(data['Lang'] == 'EN') & (data['Impressions'] >= 1)]['Page']
    st.write(urls_en)

else:
    st.warning("Veuillez uploader un fichier CSV.")
