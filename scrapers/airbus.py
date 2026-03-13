import requests
from bs4 import BeautifulSoup

def scrape():
    print("Scraping Airbus...")
    offres = []
    
    try:
        # Version TEST - À remplacer par le vrai scraping
        offres.append({
            'titre': 'Stage Data Analyst',
            'entreprise': 'Airbus',
            'contrat': 'Stage',
            'niveau_etude': 'Bac+5',
            'ville': 'Toulouse',
            'lien': 'https://www.airbus.com/careers/example',
            'date_publication': '2024-01-15'
        })
        offres.append({
            'titre': 'Ingénieur Logiciel',
            'entreprise': 'Airbus',
            'contrat': 'CDI',
            'niveau_etude': 'Bac+5',
            'ville': 'Paris',
            'lien': 'https://www.airbus.com/careers/example2',
            'date_publication': '2024-01-14'
        })
    except Exception as e:
        print(f"Erreur: {e}")
    
    return offres
