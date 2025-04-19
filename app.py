
import streamlit as st
import sqlite3
import pandas as pd

# Forbind til databasen
conn = sqlite3.connect("starwars_weapons_final.db")
cursor = conn.cursor()

# Hent unikke færdigheder
skills_query = cursor.execute("SELECT DISTINCT skill FROM weapons ORDER BY skill").fetchall()
skill_options = ["Alle"] + [s[0] for s in skills_query]

# Konfigurer Streamlit
st.set_page_config(page_title="Star Wars Våbenbrowser", layout="wide")
st.title("🔫 Star Wars RPG Våbenbrowser")

# Sektion: Tilføj nyt våben
st.subheader("➕ Tilføj nyt våben")
with st.form("add_weapon_form"):
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    name = col1.text_input("Navn")
    skill = col2.text_input("Færdighed")
    damage = col3.text_input("Skade")
    crit = col4.text_input("Crit")
    range_ = col5.text_input("Rækkevidde")
    encum = col6.text_input("Encumbrance")

    hp = col1.text_input("HP")
    restricted = col2.selectbox("Restricted", ["No", "Yes"])
    price = col3.text_input("Pris")
    rarity = col4.text_input("Sjældenhed")
    special = col5.text_input("Special")

    submitted = st.form_submit_button("Tilføj våben")

    if submitted:
        cursor.execute("""
            INSERT INTO weapons (name, skill, damage, crit, range, encum, hp, restricted, price, rarity, special)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, skill, damage, crit, range_, encum, hp, restricted, price, rarity, special))
        conn.commit()
        st.success(f"Våbenet '{name}' blev tilføjet!")

# UI: Søgning og filtre
st.subheader("🔎 Søg i våben")
col1, col2, col3 = st.columns(3)

with col1:
    search_term = st.text_input("Søg efter våben (navn eller special)", "")

with col2:
    skill_filter = st.selectbox("Filtrér efter færdighed", skill_options)

with col3:
    rarity_range = st.slider("Sjældenhed", 1, 10, (1, 10))

# SQL-forespørgsel
query = "SELECT * FROM weapons WHERE 1=1"
params = []

if search_term:
    query += " AND (name LIKE ? OR special LIKE ?)"
    params += [f"%{search_term}%", f"%{search_term}%"]

if skill_filter != "Alle":
    query += " AND skill = ?"
    params.append(skill_filter)

query += " AND rarity BETWEEN ? AND ?"
params += list(rarity_range)

# Udfør forespørgsel og vis resultater
results = pd.read_sql_query(query, conn, params=params)
st.dataframe(results, use_container_width=True)

conn.close()
