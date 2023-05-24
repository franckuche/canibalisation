import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

@st.cache
def load_data(uploaded_file):
    data = pd.read_csv(uploaded_file, delimiter = "\t")
    data['CTR'] = data['CTR'].str.replace('%', '').astype(float) / 100
    data['Impressions'] = data['Impressions'].str.replace('\u202f', '').astype(int)
    data['Clicks'] = data['Clicks'].str.replace('\u202f', '').astype(int)
    data['Lang'] = np.where(data['Page'].str.contains("/fr/"), "FR",
                      np.where(data['Page'].str.contains("/en/"), "EN", "Other"))
    return data

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    data = load_data(uploaded_file)

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
    
else:
    st.warning("Veuillez uploader un fichier CSV.")
