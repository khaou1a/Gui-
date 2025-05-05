# Importation des bibliothèques nécessaires
import streamlit as st
# Configuration de la page
st.set_page_config(page_title="DOS | DDOS DETECTION", page_icon="🔒", layout="wide")
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score
from sklearn.neighbors import KNeighborsClassifier
import concurrent.futures
import os
import math
from sequentiel_attack import run_simulation as run_sequentiel_attack_simulation


import time



# Initialisation de la page
if 'current_page' not in st.session_state:
    st.session_state.current_page = "main"



# CSS personnalisé
css = """
<style>
    .main { background-color: #000000; color: #FFFFFF; }
    .sidebar .sidebar-content { background-color: #4ADE80; color: #000000; }
    .sidebar .sidebar-content a { color: #000000; }
    .stButton>button { color: white; background-color: #4ADE80; border-radius: 5px; }
    .status-circle {
        width: 150px; height: 150px; border-radius: 50%;
        border: 15px solid #EBEBEB; margin: 10px auto;
        display: flex; align-items: center; justify-content: center;
    }
    .green-circle { background-color: #4ADE80; }
    .red-circle { background-color: #FF0000; }
    .gauge-container { width: 200px; margin: 0 auto; }
    .safe-text { color: #4ADE80; font-weight: bold; font-size: 80px; }
    .danger-text { color: #FF0000; font-weight: bold; font-size: 80px; }
    .header {
        text-align: center; font-size: 36px; font-weight: bold;
        margin-bottom: 30px; color: white;
    }
    .notification-icon {
        position: absolute; top: 20px; right: 20px; font-size: 24px;
    }
</style>
"""
st.markdown(css, unsafe_allow_html=True)


# Fonction jauge SVG
def create_gauge(value=100, max_value=100):
    angle = (value / max_value) * 180
    radians = math.radians(angle)
    end_x = 100 + 70 * math.cos(math.pi - radians)
    end_y = 100 - 70 * math.sin(math.pi - radians)

    svg = f"""
    <svg width="200" height="120" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#4ADE80;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#FFA500;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#FF0000;stop-opacity:1" />
            </linearGradient>
        </defs>
        <!-- Arc fond gris -->
        <path d="M 30 100 A 70 70 0 0 1 170 100" stroke="#EBEBEB" stroke-width="15" fill="none" />
        <!-- Arc de couleur dynamique -->
        <path d="M 30 100 A 70 70 0 0 1 {end_x:.2f} {end_y:.2f}" stroke="url(#grad)" stroke-width="15" fill="none" />
        <!-- Aiguille -->
        <line x1="100" y1="100" x2="{100 + 60 * math.cos(math.pi - radians):.2f}" y2="{100 - 60 * math.sin(math.pi - radians):.2f}" stroke="#66B2FF" stroke-width="4" />
        <circle cx="100" cy="100" r="8" fill="#66B2FF" />
    </svg>
    """
    return svg

# Fonction de navigation
def navigate_to(page_name):
    st.session_state.current_page = page_name
    if page_name == "main":
        st.session_state.current_page = "main"  # Assurer que "main" est toujours la page principale
    st.rerun()

# Fonction d'accueil
def main_page():
    with st.sidebar:
        if st.button("🏠 Home"):
            navigate_to("main")

        st.header("Detection simulation:")
        
        st.write("RUN detection ATTAQUE")
        if st.button("Séquentiel - Attaque", key="seq_attack"):
            navigate_to("sequentiel_attack")
        if st.button("Parallèle - Attaque", key="par_attack"):
            navigate_to("parallele_attack")
        
        st.write("RUN detection DOS")
        if st.button("Séquensiel-Dos", key="seq_dos"):
            navigate_to("sequentiel_dos")
        if st.button("Paralele-Dos", key="par_dos"):
            navigate_to("parallele_dos")
        
        st.write("RUN detection DDOS")
        if st.button("Séquensiel-DDos", key="seq_doss"):
            navigate_to("sequentiel_doss")
        if st.button("Paralele-DDOs", key="par_doss"):
            navigate_to("parallele_doss")
            

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<div class="header">🔒 DOS | DDOS DETECTION</div>', unsafe_allow_html=True)
        st.markdown('<div class="notification-icon">🔔</div>', unsafe_allow_html=True)
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown('<div class="status-circle green-circle"></div>', unsafe_allow_html=True)
        with col_right:
            st.markdown('<div class="status-circle green-circle"></div>', unsafe_allow_html=True)

        gauge_value = st.slider("Tester la jauge - % d'attaques détectées", 0, 100, 20)
        st.markdown(f'<div class="gauge-container">{create_gauge(gauge_value)}</div>', unsafe_allow_html=True)

        if gauge_value < 50:
            st.markdown('<div style="text-align: center;"><span class="safe-text">Safe</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: center;"><span class="danger-text">Danger</span></div>', unsafe_allow_html=True)

# Page séquentielle d'attaque
def sequentiel_attack_page():
    st.title("Détection Séquentielle des Attaques")
    if st.button("🚀 Lancer la Simulation"):
        run_sequentiel_attack_simulation()
    if st.button("Retour à l'accueil"):
        navigate_to("main")

# Pages non implémentées
def placeholder_page(title):
    st.title(title)
    st.info("Cette page est encore en construction.")
    if st.button("Retour à l'accueil"):
        navigate_to("main")


# Routage
if st.session_state.current_page == "main":
    main_page()
elif st.session_state.current_page == "sequentiel_attack":
    sequentiel_attack_page()
elif st.session_state.current_page == "parallele_attack":
    placeholder_page("Détection Parallèle des Attaques")
elif st.session_state.current_page == "sequentiel_dos":
    placeholder_page("Détection Séquentielle DOS")
elif st.session_state.current_page == "parallele_dos":
    placeholder_page("Détection Parallèle DOS")
elif st.session_state.current_page == "ddos":
    placeholder_page("Détection DDOS")
else:
    st.error("Page non reconnue.")
