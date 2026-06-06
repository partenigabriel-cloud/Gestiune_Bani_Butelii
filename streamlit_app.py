import streamlit as str
import json
import os

# Configurare pagină
str.set_page_config(page_title="Calculator Butelii & Prețuri", layout="centered")
str.title("📊 Calculator Vânzări Butelii")
str.subheader("Calculează rapid totalul de încasat pe zi/traseu")

PRETURI_FILE = "preturi_salvate.json"

def incarca_preturi():
    if os.path.exists(PRETURI_FILE):
        with open(PRETURI_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {"11kg": 0.0, "9kg": 0.0, "bg": 0.0, "ar": 0.0}
    return {"11kg": 0.0, "9kg": 0.0, "bg": 0.0, "ar": 0.0}

def salveaza_preturi(preturi):
    with open(PRETURI_FILE, "w", encoding="utf-8") as f:
        json.dump(preturi, f, indent=4, ensure_ascii=False)

# Încărcăm prețurile folosite ultima dată
preturi_salvate = incarca_preturi()

str.markdown("---")
str.markdown("### 💰 1. Setează Prețurile (RON / bucată)")
str.info("ℹ️ Prețurile introduse aici se salvează automat pentru data viitoare!")

# Punem prețurile pe 2 coloane
col_p1, col_p2 = str.columns(2)
with col_p1:
    p_11kg = str.number_input("Preț Butelie 11 kg:", min_value=0.0, value=float(preturi_salvate.get("11kg", 0.0)), step=0.5, format="%.2f")
    p_9kg = str.number_input("Preț Butelie 9 kg:", min_value=0.0, value=float(preturi_salvate.get("9kg", 0.0)), step=0.5, format="%.2f")
with col_p2:
    p_bg = str.number_input("Preț Butelie BG (guler):", min_value=0.0, value=float(preturi_salvate.get("bg", 0.0)), step=0.5, format="%.2f")
    p_ar = str.number_input("Preț Butelie AR (fără guler):", min_value=0.0, value=float(preturi_salvate.get("ar", 0.0)), step=0.5, format="%.2f")

# Salvăm dacă s-au modificat prețurile
preturi_noi = {"11kg": p_11kg, "9kg": p_9kg, "bg": p_bg, "ar": p_ar}
if preturi_noi != preturi_salvate:
    salveaza_preturi(preturi_noi)

str.markdown("---")
str.markdown("### 🛢️ 2. Introdu Cantitățile Vândute")

# Introducere cantități pe 2 coloane
col_c1, col_c2 = str.columns(2)
with col_c1:
    c_11kg = str.number_input("Bucăți 11 kg:", min_value=0, value=0, step=1)
    c_9kg = str.number_input("Bucăți 9 kg:", min_value=0, value=0, step=1)
with col_c2:
    c_bg = str.number_input("Bucăți BG (cu guler):", min_value=0, value=0, step=1)
    c_ar = str.number_input("Bucăți AR (fără guler):", min_value=0, value=0, step=1)

# Calcule parțiale
tot_11kg = c_11kg * p_11kg
tot_9kg = c_9kg * p_9kg
tot_bg = c_bg * p_bg
tot_ar = c_ar * p_ar

# Total General
total_general = tot_11kg + tot_9kg + tot_bg + tot_ar

str.markdown("---")
str.markdown("### 📋 Rezumat Calcule Parțiale")

col_r1, col_r2 = str.columns(2)
with col_r1:
    str.write(f"🔹 **11 kg:** {c_11kg} buc x {p_11kg:.2f} RON = **{tot_11kg:.2f} RON**")
    str.write(f"🔹 **9 kg:** {c_9kg} buc x {p_9kg:.2f} RON = **{tot_9kg:.2f} RON**")
with col_r2:
    str.write(f"🔺 **BG:** {c_bg} buc x {p_bg:.2f} RON = **{tot_bg:.2f} RON**")
    str.write(f"🔺 **AR:** {c_ar} buc x {p_ar:.2f} RON = **{tot_ar:.2f} RON**")

str.markdown("---")

# Afișare mare și clară pentru Totalul General
str.metric(label="💰 TOTAL GENERAL DE ÎNCASAT", value=f"{total_general:.2f} RON")

# Buton de resetare rapidă a cantităților
if str.button("🔄 Resetează Cantitățile la 0"):
    str.rerun()
