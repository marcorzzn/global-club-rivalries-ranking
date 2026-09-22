"""
scripts/utils.py
Funzioni condivise da tutti gli script del progetto RIVALITÀ.
Importare da qui — non duplicare la logica negli altri script.
"""
import unicodedata
import re


def make_id(name: str) -> str:
    """
    Genera uno slug canonico deterministico da un nome di rivalità.
    Usato in modo identico da scrape_wikipedia.py e build_ranking_data.py
    per garantire che la stessa rivalità produca sempre lo stesso id
    in entrambi i dataset.

    Esempi:
        "El Clásico"           → "el_clasico"
        "Derby della Madonnina"→ "derby_della_madonnina"
        "Fla-Flu"              → "fla_flu"
        "Old Firm"             → "old_firm"
    """
    # 1. Decomposizione Unicode → rimuove diacritici (é→e, ç→c, ñ→n, ecc.)
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')
    # 2. Lowercase
    name = name.lower()
    # 3. Tutti i caratteri non alfanumerici → underscore
    name = re.sub(r'[^a-z0-9]+', '_', name)
    # 4. Trim underscore iniziali/finali e underscore multipli
    name = name.strip('_')
    return name


def is_noise_page(title: str) -> bool:
    """
    Restituisce True se il titolo Wikipedia è probabilmente un falso positivo
    (singolo evento, lista, stagione) e non una rivalità ricorrente.

    Criteri di esclusione:
    - Contiene un anno a 4 cifre (1800-2100) MA non contiene parole-chiave di rivalità
    - Contiene "final", "qualification", "Finals" senza parole-chiave
    - Inizia con "List of" o "Football rivalries in" (pagine aggregate, non rivalità)
    """
    RIVALRY_KEYWORDS = (
        'derby', 'rivalry', 'rivalries', 'clasico', 'classico', 'clásico',
        'clássico', 'klassiker', 'classieker', 'classique', 'clasico',
        'superclasico', 'superclásico', 'el clasico', 'old firm',
    )
    low = title.lower()

    # Pagine aggregate / liste
    if title.startswith('List of') or title.startswith('Football rivalries in') \
            or title.startswith('Football derbies in') or title.startswith('Soccer rivalries in') \
            or title.startswith('Spanish football') or title.startswith('German football'):
        return True

    # Titolo che inizia con un anno → singolo evento storico
    if re.match(r'^\d{4}\b', title):
        return True

    # Anno a 4 cifre presente + nessuna parola chiave di rivalità
    has_year = bool(re.search(r'\b(18|19|20)\d{2}\b', title))
    has_rivalry_kw = any(kw in low for kw in RIVALRY_KEYWORDS)
    if has_year and not has_rivalry_kw:
        return True

    # Parole di singolo evento senza keyword rivalità
    single_event_words = ('final', 'finals', 'qualification', 'qualifier',
                          'tournament', 'championship', 'season', 'cup final')
    if any(w in low for w in single_event_words) and not has_rivalry_kw:
        return True

    return False
