import streamlit as st
from datetime import datetime
import os
import matplotlib.pyplot as plt
from collections import Counter
import random

st.set_page_config(page_title="Min Digitale Dagbog", layout="centered")
st.title("📓 Min Digitale Dagbog")
st.write("Velkommen! Skriv dine tanker og vælg en stemning:")

stemninger = {
    "😊 Glad": "😊",
    "😢 Trist": "😢",
    "😠 Frustreret": "😠",
    "😴 Træt": "😴",
    "😐 Neutral": "😐",
    "😍 Forelsket": "😍"
}

refleksioner = [
    "Hvad lærte du om dig selv i dag?",
    "Hvordan kan du bruge det du følte i dag, i morgen?",
    "Er der noget du gerne ville have gjort anderledes?",
    "Hvad gjorde dig glad i dag?",
    "Hvordan passer du på dig selv i svære perioder?"
]

stemning = st.selectbox("Vælg stemning", list(stemninger.keys()))
tekst = st.text_area("Skriv dit dagbogsindlæg:")

if st.button("Gem indlæg"):
    if tekst.strip() != "":
        nu = datetime.now()
        filnavn = f"dagbog_{nu.strftime('%Y-%m-%d')}.txt"
        med_tid = f"{nu.strftime('%H:%M:%S')} – Stemning: {stemninger[stemning]} {stemning}\n{tekst}\n{'-'*40}\n"
        with open(filnavn, "a", encoding="utf-8") as fil:
            fil.write(med_tid)
        st.success("✅ Indlæg gemt!")
        st.info(f"💬 Refleksion: {random.choice(refleksioner)}")
    else:
        st.warning("⚠️ Du har ikke skrevet noget endnu.")

st.divider()
st.header("📊 Stemningsstatistik")

# Statistikknapper
col1, col2 = st.columns(2)

with col1:
    if st.button("Vis søjlediagram"):
        stemningstæller = Counter()
        for filnavn in os.listdir():
            if filnavn.startswith("dagbog_") and filnavn.endswith(".txt"):
                with open(filnavn, "r", encoding="utf-8") as fil:
                    linjer = fil.readlines()
                    for linje in linjer:
                        if "Stemning:" in linje:
                            for emoji in stemninger.values():
                                if emoji in linje:
                                    stemningstæller[emoji] += 1
        if stemningstæller:
            fig, ax = plt.subplots()
            ax.bar(stemningstæller.keys(), stemningstæller.values(), color="skyblue")
            ax.set_title("Stemninger fordelt på antal")
            st.pyplot(fig)
        else:
            st.info("Ingen stemningsdata fundet endnu.")

with col2:
    if st.button("Vis udvikling over tid"):
        datoer = []
        stemningsliste = []
        for filnavn in sorted(os.listdir()):
            if filnavn.startswith("dagbog_") and filnavn.endswith(".txt"):
                dato = filnavn.replace("dagbog_", "").replace(".txt", "")
                with open(filnavn, "r", encoding="utf-8") as fil:
                    for linje in fil:
                        if "Stemning:" in linje:
                            for navn, emoji in stemninger.items():
                                if emoji in linje:
                                    datoer.append(dato)
                                    stemningsliste.append(navn)
                                    break
                            break
        if datoer:
            fig, ax = plt.subplots()
            ax.plot(datoer, stemningsliste, marker="o", linestyle="-", color="#4477aa")
            ax.set_title("Stemning over tid")
            ax.set_xlabel("Dato")
            ax.set_ylabel("Stemning")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.info("Ingen data til graf over tid endnu.")