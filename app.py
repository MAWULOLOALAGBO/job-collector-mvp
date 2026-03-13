import streamlit as st
from database import get_all_offres
import os

st.set_page_config(
    page_title="Job Collector MVP",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Recherche d'offres d'emploi")
st.markdown("Offres collectées directement sur les sites des entreprises")

# Vérifier si la BDD existe
if not os.path.exists("data/offres.db"):
    st.warning("🚧 La base de données n'est pas encore prête. Le premier scraping va bientôt commencer automatiquement.")
    st.info("⏱️ Reviens dans quelques minutes, les offres apparaîtront ici !")
    st.stop()

# Charger les données
df = get_all_offres()

if df.empty:
    st.warning("Aucune offre disponible pour le moment. Le scraping automatique va bientôt s'exécuter.")
    st.stop()

# Sidebar pour les filtres
st.sidebar.header("🔍 Filtres")

# Filtres
contrat = st.sidebar.multiselect(
    "Type de contrat",
    options=df['contrat'].unique() if not df.empty else []
)

ville = st.sidebar.multiselect(
    "Ville",
    options=df['ville'].unique() if not df.empty else []
)

# Appliquer les filtres
filtered_df = df.copy()
if contrat:
    filtered_df = filtered_df[filtered_df['contrat'].isin(contrat)]
if ville:
    filtered_df = filtered_df[filtered_df['ville'].isin(ville)]

# Affichage
st.header(f"📊 {len(filtered_df)} offres trouvées")

for _, row in filtered_df.iterrows():
    with st.expander(f"{row['titre']} - {row['entreprise']}"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Contrat:** {row['contrat']}")
        with col2:
            st.write(f"**Ville:** {row['ville']}")
        with col3:
            st.write(f"**Publié:** {row['date_publication']}")
        
        st.write(f"**Niveau:** {row['niveau_etude']}")
        st.markdown(f"**[👉 Postuler]({row['lien']})**")
