import time
import re
import pandas as pd
from bs4 import BeautifulSoup

class TrophyScraper:
    def __init__(self):
        # cloudscraper per bypassare le protezioni anti-bot di Transfermarkt (es. Cloudflare)
        try:
            import cloudscraper
            self.scraper = cloudscraper.create_scraper(browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            })
        except ImportError:
            print("ATTENZIONE: Modulo 'cloudscraper' non installato. Esegui: pip install cloudscraper")
            self.scraper = None

        # Configurazione SPARQL per Wikidata come meccanismo di fallback
        try:
            from SPARQLWrapper import SPARQLWrapper, JSON
            self.sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
            # Wikidata richiede un User-Agent esplicito per non bloccare le richieste
            self.sparql.agent = "RivalryIndexScraper/1.0 (https://github.com/marcorzzn; your@email.com) SPARQLWrapper"
        except ImportError:
            print("ATTENZIONE: Modulo 'SPARQLWrapper' non installato. Esegui: pip install SPARQLWrapper")
            self.sparql = None

    def scrape_transfermarkt_trophies(self, team_name):
        """
        Interroga Transfermarkt bypassando Cloudflare tramite cloudscraper.
        """
        if not self.scraper:
            raise RuntimeError("cloudscraper non disponibile.")

        print(f"Scraping Transfermarkt per {team_name}...")
        search_url = f"https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={team_name}"
        
        # 1. Trova l'URL della squadra
        response = self.scraper.get(search_url)
        if response.status_code != 200:
            raise Exception(f"Errore Transfermarkt search: HTTP {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        result_table = soup.find('table', {'class': 'items'})
        if not result_table:
            raise Exception("Nessun team trovato nella ricerca su Transfermarkt.")
            
        first_row = result_table.find('tbody').find('tr')
        team_link_tag = first_row.find('a', href=True)
        if not team_link_tag:
            raise Exception("Impossibile estrarre l'URL del team da Transfermarkt.")
            
        team_href = team_link_tag['href']
        
        # 2. Costruisci l'URL per la pagina dei successi
        success_url = "https://www.transfermarkt.com" + team_href.replace("startseite", "erfolge")
        
        time.sleep(1.5) # Rispetto per il server anche se bypassiamo CF
        
        # 3. Estrai i trofei
        resp_succ = self.scraper.get(success_url)
        if resp_succ.status_code != 200:
            raise Exception(f"Errore Transfermarkt successi: HTTP {resp_succ.status_code}")

        soup_succ = BeautifulSoup(resp_succ.text, 'html.parser')
        total = 0
        
        success_boxes = soup_succ.find_all('div', {'class': 'box'})
        for box in success_boxes:
            header = box.find('h2')
            # Cerca box che contengono competizioni vinte (solitamente indicano 'Winner' o 'Champion')
            if header and ('Winner' in header.text or 'Champion' in header.text or 'Sieger' in header.text):
                header_text = header.text.strip()
                match = re.search(r'(\d+)x', header_text)
                if match:
                    total += int(match.group(1))
                    
        return total

    def scrape_wikidata_trophies(self, team_name):
        """
        Fallback solido via Wikidata API.
        Cerca la squadra e conta i titoli vinti (P1346) per competizioni di massimo livello.
        """
        if not self.sparql:
            raise RuntimeError("SPARQLWrapper non disponibile.")

        print(f"Fallback su Wikidata per {team_name}...")
        
        # 1. Trova il Q-id della squadra di calcio
        # Q476028 è "association football club"
        search_query = f"""
        SELECT ?item WHERE {{
          ?item wdt:P31/wdt:P279* wd:Q476028.
          ?item rdfs:label "{team_name}"@en.
        }}
        LIMIT 1
        """
        self.sparql.setQuery(search_query)
        self.sparql.setReturnFormat("json")
        results = self.sparql.query().convert()
        
        bindings = results["results"]["bindings"]
        if not bindings:
            # Fallback a ricerca testuale più ampia se il nome esatto fallisce
            search_query_broad = f"""
            SELECT ?item WHERE {{
              ?item wdt:P31/wdt:P279* wd:Q476028.
              ?item rdfs:label ?label.
              FILTER(CONTAINS(LCASE(?label), LCASE("{team_name}")))
              FILTER(LANG(?label) = "en")
            }}
            LIMIT 1
            """
            self.sparql.setQuery(search_query_broad)
            results = self.sparql.query().convert()
            bindings = results["results"]["bindings"]
            
            if not bindings:
                raise Exception(f"Impossibile trovare l'entità Wikidata per {team_name}.")

        team_qid = bindings[0]["item"]["value"].split("/")[-1]
        
        # 2. Conta le vittorie (P1346) in cui il team è il vincitore
        # Nota: in Wikidata le competizioni hanno la proprietà P1346 (winner) che punta alla squadra
        count_query = f"""
        SELECT (COUNT(?competition) AS ?trophies) WHERE {{
          ?competition wdt:P1346 wd:{team_qid}.
          # Opzionale: potremmo filtrare solo per tornei specifici se necessario, ma di base conta tutte le vittorie
        }}
        """
        self.sparql.setQuery(count_query)
        self.sparql.setReturnFormat("json")
        count_res = self.sparql.query().convert()
        
        total_trophies = int(count_res["results"]["bindings"][0]["trophies"]["value"])
        return total_trophies

def update_teams_metadata_with_trophies(metadata_csv_path, error_log_file="scraper_errors.txt"):
    """
    Legge il CSV, scarica in parallelo i trofei gestendo fallimenti tramite eccezioni
    che loggano su file e procedono senza crashare lo script.
    """
    try:
        df = pd.read_csv(metadata_csv_path)
    except FileNotFoundError:
        print(f"Errore: File {metadata_csv_path} non trovato.")
        return

    scraper = TrophyScraper()
    print("Inizio aggiornamento trofei (Prestigio T)...")
    
    for idx, row in df.iterrows():
        team = row['team_name']
        trophies = 0
        success = False
        
        # Strategia 1: Transfermarkt via cloudscraper
        try:
            trophies = scraper.scrape_transfermarkt_trophies(team)
            success = True
            print(f"--> [OK] {team}: {trophies} trofei (Transfermarkt).")
        except Exception as e_tm:
            msg = f"Transfermarkt fallito per {team}: {e_tm}"
            print(f"    [!] {msg}")
            with open(error_log_file, "a") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")
            
            # Strategia 2: Fallback Wikidata via SPARQL
            try:
                trophies = scraper.scrape_wikidata_trophies(team)
                success = True
                print(f"--> [OK] {team}: {trophies} trofei (Wikidata).")
            except Exception as e_wd:
                msg2 = f"Wikidata fallito per {team}: {e_wd}"
                print(f"    [!] {msg2}")
                with open(error_log_file, "a") as f:
                    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg2}\n")
        
        if success and trophies > 0:
            df.at[idx, 'total_major_trophies'] = trophies
        elif not success:
            # Assegna 0 in caso di fallimento totale per non rompere il modello matematico (verrà normalizzato)
            df.at[idx, 'total_major_trophies'] = 0
            
        time.sleep(2) # Rispetto rate limits
        
    df.to_csv(metadata_csv_path, index=False)
    print("Metadati aggiornati e salvati. Controlla scraper_errors.txt per eventuali fallimenti.")

if __name__ == "__main__":
    import os
    if os.path.exists("teams_metadata.csv"):
        update_teams_metadata_with_trophies("teams_metadata.csv")
    else:
        print("Il file teams_metadata.csv non esiste ancora. Esegui prima etl_pipeline.py")
