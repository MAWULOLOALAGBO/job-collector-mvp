import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = "data/offres.db"

def init_database():
    """Crée le dossier data et la table si nécessaire"""
    os.makedirs("data", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS offres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT,
            entreprise TEXT,
            contrat TEXT,
            niveau_etude TEXT,
            ville TEXT,
            lien TEXT,
            date_publication TEXT,
            date_scraping TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_offres(offres_list):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    for offre in offres_list:
        c.execute('''
            INSERT INTO offres 
            (titre, entreprise, contrat, niveau_etude, ville, lien, date_publication, date_scraping)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            offre.get('titre', ''),
            offre.get('entreprise', ''),
            offre.get('contrat', ''),
            offre.get('niveau_etude', ''),
            offre.get('ville', ''),
            offre.get('lien', ''),
            offre.get('date_publication', ''),
            datetime.now().isoformat()
        ))
    
    conn.commit()
    conn.close()

def get_all_offres():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM offres ORDER BY date_scraping DESC", conn)
    conn.close()
    return df
