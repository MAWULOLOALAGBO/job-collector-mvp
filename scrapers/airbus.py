# scrapers/airbus.py
import re
import time
from playwright.sync_api import sync_playwright

def scrape():
    """Scrape les vraies offres Airbus"""
    print("🚁 Scraping des vraies offres Airbus...")
    offres = []
    
    try:
        with sync_playwright() as p:
            # Lancer le navigateur (mode headless = invisible)
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Aller sur la page carrière
            url = "https://ag.wd3.myworkdayjobs.com/fr-FR/Airbus"
            print(f"🌐 Accès à {url}")
            page.goto(url, timeout=30000)
            
            # Attendre que la page charge
            page.wait_for_selector('[data-automation-id="jobTitle"]', timeout=10000)
            
            # Faire défiler pour charger plus d'offres
            for i in range(3):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)
            
            # Récupérer toutes les offres
            jobs = page.query_selector_all('[data-automation-id="jobTitle"]')
            print(f"📊 {len(jobs)} offres trouvées")
            
            # Pour chaque offre, extraire les infos
            for job in jobs[:20]:  # Limite à 20 offres pour commencer
                try:
                    # Titre du poste
                    titre_elem = job.query_selector('a')
                    titre = titre_elem.inner_text() if titre_elem else "Titre inconnu"
                    
                    # Lien
                    lien = titre_elem.get_attribute('href') if titre_elem else ""
                    if lien and not lien.startswith('http'):
                        lien = f"https://ag.wd3.myworkdayjobs.com{lien}"
                    
                    # Remonter au conteneur parent pour avoir plus d'infos
                    parent = job.evaluate("el => el.closest('li')")
                    
                    if parent:
                        # Aller chercher les infos dans le parent
                        page_parent = page.locator(f'xpath=//li[.//*[contains(text(), "{titre[:20]}")]]').first
                        
                        # Extraire la localisation
                        location_elem = page_parent.locator('[data-automation-id="locations"]').first
                        location = location_elem.inner_text() if location_elem.count() > 0 else "Non spécifié"
                        
                        # Extraire la date
                        date_elem = page_parent.locator('[data-automation-id="postedOn"]').first
                        date_text = date_elem.inner_text() if date_elem.count() > 0 else ""
                        
                        # Nettoyer la date
                        date_publication = nettoyer_date(date_text)
                        
                        # Déterminer le type de contrat
                        contrat = determiner_contrat(titre)
                        
                        # Déterminer le niveau d'étude
                        niveau = determiner_niveau(titre)
                        
                        offre = {
                            'titre': titre,
                            'entreprise': 'Airbus',
                            'contrat': contrat,
                            'niveau_etude': niveau,
                            'ville': location.replace("Area", "").strip(),
                            'lien': lien,
                            'date_publication': date_publication
                        }
                        offres.append(offre)
                        print(f"  ✅ {titre[:50]}...")
                    
                except Exception as e:
                    print(f"  ❌ Erreur sur une offre: {e}")
                    continue
            
            browser.close()
            
    except Exception as e:
        print(f"❌ Erreur globale: {e}")
        # Fallback : si Playwright échoue, on retourne des offres de test
        print("⚠️ Utilisation des offres de test")
        offres = get_test_offres()
    
    print(f"✅ Total: {len(offres)} offres récupérées")
    return offres

def nettoyer_date(date_text):
    """Convertit 'Publié aujourd'hui' en date réelle"""
    from datetime import datetime, timedelta
    
    if "aujourd'hui" in date_text.lower():
        return datetime.now().strftime("%Y-%m-%d")
    elif "hier" in date_text.lower():
        return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        # Essaie d'extraire une date
        import re
        match = re.search(r'\d{1,2}/\d{1,2}/\d{4}', date_text)
        if match:
            return match.group()
        return datetime.now().strftime("%Y-%m-%d")

def determiner_contrat(titre):
    """Détermine le type de contrat à partir du titre"""
    titre_lower = titre.lower()
    if "apprenti" in titre_lower or "alt" in titre_lower:
        return "Alternance"
    elif "stage" in titre_lower or "intern" in titre_lower:
        return "Stage"
    elif "werkstudent" in titre_lower:
        return "Stage"
    elif "cdi" in titre_lower or "permanent" in titre_lower:
        return "CDI"
    elif "cdd" in titre_lower or "fixed term" in titre_lower:
        return "CDD"
    else:
        return "Non spécifié"

def determiner_niveau(titre):
    """Détermine le niveau d'étude à partir du titre"""
    titre_lower = titre.lower()
    if "apprenti" in titre_lower or "alt" in titre_lower:
        return "Bac+3 à Bac+5"
    elif "stage" in titre_lower or "intern" in titre_lower:
        return "Bac+3 à Bac+5"
    elif "senior" in titre_lower or "lead" in titre_lower:
        return "Bac+5 minimum"
    elif "junior" in titre_lower:
        return "Bac+3 minimum"
    else:
        return "Non spécifié"

def get_test_offres():
    """Offres de test en cas d'échec"""
    return [
        {
            'titre': 'Stage Data Analyst',
            'entreprise': 'Airbus',
            'contrat': 'Stage',
            'niveau_etude': 'Bac+5',
            'ville': 'Toulouse',
            'lien': 'https://www.airbus.com/careers/example1',
            'date_publication': '2024-01-15'
        },
        {
            'titre': 'Ingénieur Logiciel',
            'entreprise': 'Airbus',
            'contrat': 'CDI',
            'niveau_etude': 'Bac+5',
            'ville': 'Paris',
            'lien': 'https://www.airbus.com/careers/example2',
            'date_publication': '2024-01-14'
        }
    ]
