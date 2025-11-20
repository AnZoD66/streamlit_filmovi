import streamlit as st
import pandas as pd
from učitaj import ucitaj_podatke

SHEET_URL = st.secrets["sheet_url"]
SHEET_NAME = "filmovi"
df, worksheet = ucitaj_podatke(SHEET_URL, SHEET_NAME)

df["Godina"] = pd.to_numeric(df["Godina"])
df["Ocjena"] = pd.to_numeric(df["Ocjena"])

st.title("Moji omiljeni filmovi")

st.subheader("Trenutni opis filmova")
st.dataframe(df)

st.subheader("Dodaj novi film")
naslov = st.text_input("Naslov")
godina = st.number_input("Godina", step = 1, format = "%d")
žanr = st.text_input("Žanr")
ocjena = st.slider("Ocjena", 1, 10)

if st.button("Dodaj film") == True:
    novi_red = [naslov, int(godina), žanr, ocjena]
    worksheet.append_row(novi_red)
    st.success("Film je uspješno dodan!")
    st.rerun()

st.subheader("Pretraži filmove")
filtrirani = df.copy()

žanr_filt = st.text_input("Pretraži po žanru")
godina_filt = st.number_input("Pretraži po godini", step = 1, format = "%d")

if žanr_filt:
    filtrirani = filtrirani[filtrirani["Žanr"].str.contains(žanr_filt, case = False)]

if godina_filt:
    filtrirani = filtrirani[filtrirani["Godina"] == int(godina_filt)]

st.dataframe(filtrirani)

st.subheader("Brisanje filmova")

filmovi_opcije = df.apply(lambda row: f"{row["Naslov"]} ({row["Godina"]})", axis = 1).tolist()
film_za_brisanje = st.selectbox("Odaberi film za brisanje", options = filmovi_opcije)

if st.button("Izbriši film"):
    for idx, row in df.iterrows():
        if f"{row["Naslov"]} ({row["Godina"]})" == film_za_brisanje:
            worksheet.delete_rows(idx + 2)
            st.success("Film je uspješno obrisan")
            st.rerun()

st.subheader("Top 3 filma")

top3 = df.sort_values(by = "Ocjena", ascending = False).head(3)
st.table(top3)
