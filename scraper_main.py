import importlib
from database import init_database, save_offres
from config import ENTREPRISES

def run_all_scrapers():
    print("🚀 Démarrage du scraping...")
    init_database()
    
    for entreprise in ENTREPRISES:
        print(f"\n📋 Traitement de {entreprise['nom']}...")
        
        try:
            # Pour l'instant on utilise le module airbus
            if entreprise['nom'] == "Airbus":
                from scrapers import airbus
                offres = airbus.scrape()
            
            if offres:
                save_offres(offres)
                print(f"✅ {len(offres)} offres sauvegardées")
            else:
                print(f"⚠️ Aucune offre trouvée")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    print("\n✅ Scraping terminé!")

if __name__ == "__main__":
    run_all_scrapers()
