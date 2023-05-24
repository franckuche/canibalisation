import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Analyseur de données SEO")

uploaded_file = st.file_uploader("Veuillez envoyer votre fichier CSV", type=['csv'])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, thousands=' ', decimal=',')
    
    # Conversion des colonnes 'Clicks' et 'Impressions' en entiers
    data['Clicks'] = data['Clicks'].str.replace('\u202f', '').astype(int)
    data['Impressions'] = data['Impressions'].str.replace('\u202f', '').astype(int)

    # Conversion de la colonne 'CTR' en décimal, après avoir supprimé le signe '%'
    data['CTR'] = pd.to_numeric(data['CTR'].str.replace('%', ''), errors='coerce') / 100

    # Ajout d'une nouvelle colonne 'Lang' pour identifier la langue de la page
    data['Lang'] = np.where(data['Page'].str.contains("/fr/"), "FR",
                        np.where(data['Page'].str.contains("/en/"), "EN", "Autre"))


    # Affichage du nombre de pages par langue
    st.subheader("Nombre de pages par langue")
    fig, ax = plt.subplots()
    data['Lang'].value_counts().plot(kind='bar', ax=ax)
    st.pyplot(fig)

    # Affichage des mots-clés qui rankent à la fois en français et en anglais
    st.subheader("Mots-clés qui rankent à la fois en français et en anglais")
    keywords_fr_en = data[data['Lang'].isin(['FR', 'EN'])]['Query'].value_counts()
    st.write(keywords_fr_en[keywords_fr_en > 1])

else:
    st.warning("Veuillez uploader un fichier CSV.")
