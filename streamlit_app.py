import streamlit as st
import json
import os

# Configurare pagină
st.set_page_config(page_title="Calculator Butelii Simplu", layout="centered", page_icon="📊")
st.title("📊 Calculator Vânzări Butelii")
st.subheader("Calculează rapid totalul de încasat pe zi/traseu")

PRETURI_FILE = "preturi_salvate_simplu.json"

def incarca_preturi():
    if os.path.exists(PRETURI_FILE):
        with open(PRETURI_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {"11kg": 0.0, "9kg": 0.0}
    return {"11kg": 0.0, "9kg": 0.0}

def salveaza_preturi(preturi):
    with open(PRETURI_FILE, "w", encoding="utf-8") as f:
        json.dump(preturi, f, indent=4, ensure_ascii=False)

# Funcție pentru resetarea completă a cantităților din memorie
def reset_cantitati():
    st.session_state["c_11kg"] = 0
    st.session_state["c_9kg"] = 0
    st.session_state["def_11kg"] = 0
    st.session_state["def_9kg"] = 0

# Încărcăm prețurile folosite ultima dată
preturi_salvate = incarca_preturi()

st.markdown("---")
st.markdown("### 💰 1. Setează Prețurile (RON / bucată)")
st.info("ℹ️ Prețurile introduse aici se salvează automat pentru data viitoare!")

# Setați prețurile pe 2 coloane (doar pentru 11kg și 9kg)
col_p1, col_p2 = st.columns(2)
with col_p1:
    p_11kg = st.number_input("Preț Butelie 11 kg:", min_value=0.0, value=float(preturi_salvate.get("11kg", 0.0)), step=0.5, format="%.2f")
with col_p2:
    p_9kg = st.number_input("Preț Butelie 9 kg:", min_value=0.0, value=float(preturi_salvate.get("9kg", 0.0)), step=0.5, format="%.2f")

# Salvăm dacă s-au modificat prețurile
preturi_noi = {"11kg": p_11kg, "9kg": p_9kg}
if preturi_noi != preturi_salvate:
    salveaza_preturi(preturi_noi)

st.markdown("---")
st.markdown("### 🛢️ 2. Introdu Cantitățile Vândute (Cu încasare)")

# Inițializăm variabilele în memorie dacă nu există
if "c_11kg" not in st.session_state: st.session_state["c_11kg"] = 0
if "c_9kg" not in st.session_state: st.session_state["c_9kg"] = 0
if "def_11kg" not in st.session_state: st.session_state["def_11kg"] = 0
if "def_9kg" not in st.session_state: st.session_state["def_9kg"] = 0

# Introducere cantități bune (pe care iei bani)
col_c1, col_c2 = st.columns(2)
with col_c1:
    c_11kg = st.number_input("Bucăți 11 kg standard:", min_value=0, step=1, key="c_11kg")
with col_c2:
    c_9kg = st.number_input("Bucăți 9 kg standard:", min_value=0, step=1, key="c_9kg")

st.markdown("---")
st.markdown("### 🛠️ 3. Schimburi pe Garanție / Butelii Defecte (0 RON)")
st.warning("⚠️ Aceste butelii se contorizează la bucăți descărcate, dar NU se adaugă la bani!")

# Introducere butelii defecte
col_d1, col_d2 = st.columns(2)
with col_d1:
    def_11kg = st.number_input("Defecte / Schimb 11 kg:", min_value=0, step=1, key="def_11kg")
with col_d2:
    def_9kg = st.number_input("Defecte / Schimb 9 kg:", min_value=0, step=1, key="def_9kg")

# Calcule parțiale (doar pe cele bune)
tot_11kg = c_11kg * p_11kg
tot_9kg = c_9kg * p_9kg

# Total General Bani
total_general = tot_11kg + tot_9kg

st.markdown("---")
st.markdown("### 📋 Rezumat Traseu")

col_r1, col_r2 = st.columns(2)
with col_r1:
    st.write(f"🔹 **Vândut 11 kg:** {c_11kg} buc = **{tot_11kg:.2f} RON**")
    st.write(f"🔹 **Vândut 9 kg:** {c_9kg} buc = **{tot_9kg:.2f} RON**")
with col_r2:
    st.write(f"🛠️ **Defecte 11 kg (schimb):** {def_11kg} buc = **0.00 RON**")
    st.write(f"🛠️ **Defecte 9 kg (schimb):** {def_9kg} buc = **0.00 RON**")

# Total bucăți fizice descărcate din mașină
total_bucati_11kg = c_11kg + def_11kg
total_bucati_9kg = c_9kg + def_9kg

st.info(f"🚚 **Total butelii fizice predate:** {total_bucati_11kg} de 11kg și {total_bucati_9kg} de 9kg.")

st.markdown("---")

# Afișare mare și clară pentru Totalul de Încasat (Bani gheață/card)
st.metric(label="💰 TOTAL GENERAL DE ÎNCASAT", value=f"{total_general:.2f} RON")

st.markdown("---")
# Buton de resetare care golește tot
st.button("🔄 Resetează Toate Cantitățile", on_click=reset_cantitati)
