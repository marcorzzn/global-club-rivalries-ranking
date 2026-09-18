import os
import requests
import pandas as pd
import time

def fetch_wikipedia_logo(team_name, output_dir):
    """
    Interroga le Action API di Wikipedia per trovare l'immagine principale (solitamente il logo)
    associata alla pagina della squadra e la scarica in locale.
    """
    session = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"
    
    # Step 1: Cerca la pagina esatta tramite opensearch (per gestire le ambiguità, es. "Juventus F.C.")
    search_params = {
        "action": "opensearch",
        "search": team_name,
        "limit": 1,
        "namespace": 0,
        "format": "json"
    }
    
    try:
        search_res = session.get(url=url, params=search_params).json()
        if not search_res[1]:
            print(f"  [!] Pagina Wikipedia non trovata per '{team_name}'.")
            return False
            
        page_title = search_res[1][0]
        
        # Step 2: Estrai l'immagine originale associata alla pagina
        image_params = {
            "action": "query",
            "format": "json",
            "prop": "pageimages",
            "titles": page_title,
            "piprop": "original"
        }
        
        img_res = session.get(url=url, params=image_params).json()
        pages = img_res.get("query", {}).get("pages", {})
        
        for page_id, page_data in pages.items():
            if "original" in page_data:
                img_url = page_data["original"]["source"]
                
                # Accettiamo idealmente SVG o PNG (Wikipedia Commons usa molto gli SVG per i loghi)
                ext = img_url.split('.')[-1].lower()
                if ext not in ['svg', 'png', 'jpg', 'jpeg']:
                    ext = 'png' # Fallback fittizio
                
                # Salvataggio del file
                file_name = f"{team_name.replace(' ', '_').replace('/', '_')}.{ext}"
                file_path = os.path.join(output_dir, file_name)
                
                # Scarica l'immagine
                img_data = requests.get(img_url).content
                with open(file_path, 'wb') as f:
                    f.write(img_data)
                
                print(f"  [OK] Logo scaricato per '{team_name}': {file_name}")
                return True
                
        print(f"  [!] Nessuna immagine 'originale' (logo) trovata per '{team_name}' nell'API.")
        return False
        
    except Exception as e:
        print(f"  [!] Errore API per '{team_name}': {e}")
        return False

def export_top_rivalry_logos(csv_path="top_rivalries.csv", top_n=20):
    """
    Legge il CSV di output del modello di rivalità, estrae le squadre
    delle Top N rivalità e ne scarica i loghi isolati.
    """
    if not os.path.exists(csv_path):
        print(f"Errore: Il file {csv_path} non esiste.")
        print("Assicurati di aver fatto esportare il CSV al file rivalry_model.py (es. results.to_csv('top_rivalries.csv')).")
        return

    print(f"Caricamento {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Prendi le prime N rivalità
    top_df = df.head(top_n)
    
    # Estrai una lista unica di tutte le squadre coinvolte in queste Top 20
    unique_teams = pd.concat([top_df['team_1'], top_df['team_2']]).unique()
    
    # Crea cartella /assets/logos
    output_dir = os.path.join("assets", "logos")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Inizio estrazione loghi per {len(unique_teams)} squadre...")
    
    missing_logos = []
    
    for team in unique_teams:
        success = fetch_wikipedia_logo(team, output_dir)
        if not success:
            missing_logos.append(team)
        time.sleep(1) # Rate limiting di cortesia verso Wikimedia
        
    print("\n--- Download Completato ---")
    if missing_logos:
        print(f"Non è stato possibile trovare i loghi per le seguenti {len(missing_logos)} squadre:")
        for t in missing_logos:
            print(f"- {t}")
        print("Ti consigliamo di cercarli manualmente su Google Immagini (formato SVG/PNG trasparente).")
    else:
        print("Tutti i loghi sono stati scaricati con successo!")

if __name__ == "__main__":
    export_top_rivalry_logos("top_rivalries.csv", top_n=20)
