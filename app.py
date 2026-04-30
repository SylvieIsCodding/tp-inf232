import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import date

# --- CONFIGURATION ---
st.set_page_config(page_title="AAC-Learn Tracker", page_icon="🧩", layout="wide")
DATA_FILE = "aac_data.csv"

# --- DATA MANAGEMENT ---
# Initialize the dataset if it doesn't exist
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Duration (min)", "Words Used", "Initiation Type", "Emotion"])

def save_data(date_val, duration, words, init_type, emotion):
    df = load_data()
    new_data = pd.DataFrame([{
        "Date": date_val, 
        "Duration (min)": duration, 
        "Words Used": words, 
        "Initiation Type": init_type, 
        "Emotion": emotion
    }])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# --- APP UI ---
st.title("🧩 AAC-Learn: Autism Communication Tracker")
st.markdown("Application de collecte et d'analyse des progrès d'apprentissage via outil CAA (Communication Améliorée et Alternative).")

# Create tabs for the app
tab1, tab2, tab3 = st.tabs(["📝 Collecte de Données", "📊 Analyse Descriptive", "📂 Base de Données"])

# --- TAB 1: DATA COLLECTION ---
with tab1:
    st.header("Enregistrer une nouvelle session")
    with st.form("data_collection_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            session_date = st.date_input("Date de la session", date.today())
            duration = st.number_input("Durée d'utilisation (en minutes)", min_value=1, max_value=300, value=30)
            words_used = st.number_input("Nombre de mots/symboles utilisés", min_value=0, max_value=500, value=5)
            
        with col2:
            init_type = st.selectbox("Type d'initiation principale", ["Spontanée", "Guidée", "Imitation"])
            emotion = st.selectbox("État émotionnel dominant", ["Engagé/Intéressé", "Calme", "Frustré", "Fatigué"])
            
        submit = st.form_submit_button("💾 Enregistrer les données")
        
        if submit:
            save_data(session_date, duration, words_used, init_type, emotion)
            st.success("Données enregistrées avec succès !")
            st.rerun() # Refresh the app to update charts

# --- TAB 2: DESCRIPTIVE ANALYSIS ---
with tab2:
    st.header("Analyse Descriptive des Progrès")
    
    if df.empty:
        st.info("Aucune donnée disponible. Veuillez enregistrer une session dans l'onglet 'Collecte de Données'.")
    else:
        # Convert date column to datetime for plotting
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Key Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total des sessions", len(df))
        col2.metric("Mots totaux utilisés", df["Words Used"].sum())
        col3.metric("Durée moyenne (min)", round(df["Duration (min)"].mean(), 1))
        
        st.divider()
        
        # Charts using Plotly for "Robustness and Efficiency"
        colA, colB = st.columns(2)
        
        with colA:
            # Line chart: Words over time
            fig_words = px.line(df.groupby('Date').sum(numeric_only=True).reset_index(), 
                                x='Date', y='Words Used', markers=True, 
                                title="Évolution de l'utilisation des mots/symboles")
            st.plotly_chart(fig_words, use_container_width=True)
            
            # Pie chart: Emotion
            fig_emotion = px.pie(df, names='Emotion', title="Répartition des états émotionnels", hole=0.4)
            st.plotly_chart(fig_emotion, use_container_width=True)

        with colB:
            # Bar chart: Initiation type
            fig_init = px.histogram(df, x='Initiation Type', color='Initiation Type',
title="Types d'initiation à la communication")
            st.plotly_chart(fig_init, use_container_width=True)
            
            # Scatter plot: Duration vs Words Used (Preparation for linear regression!)
            fig_scatter = px.scatter(df, x='Duration (min)', y='Words Used', color='Emotion',
                                     title="Relation entre la durée et les mots utilisés")
            st.plotly_chart(fig_scatter, use_container_width=True)

# --- TAB 3: RAW DATA ---
with tab3:
    st.header("Aperçu des Données Brutes")
    st.dataframe(df, use_container_width=True)
    
    # Download button for reliability
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Télécharger les données (CSV)",
            data=csv,
            file_name='aac_learning_data.csv',
            mime='text/csv',
        )



