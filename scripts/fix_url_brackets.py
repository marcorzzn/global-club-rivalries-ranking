import json, re, urllib.parse

with open('data/logos.json', encoding='utf-8') as f:
    logos = json.load(f)

fixed = 0
for team, url in list(logos.items()):
    if '%5B%5BFile%3A' in url or '%5B%5BImage%3A' in url:
        # Decodifica l'URL, estrai solo il nome del file
        decoded = urllib.parse.unquote(url)
        # Pattern: ...Redirect/file/[[File:NOME_FILE.ext&width=...
        m = re.search(r'Redirect/file/\[\[(?:File|Image):([^&\]]+)', decoded, re.IGNORECASE)
        if m:
            filename = m.group(1).strip()
            encoded = urllib.parse.quote(filename.replace(' ', '_'))
            new_url = f'https://en.wikipedia.org/w/index.php?title=Special:Redirect/file/{encoded}&width=300'
            print(f'FIX {team}:')
            print(f'  OLD: {url[:80]}')
            print(f'  NEW: {new_url[:80]}')
            logos[team] = new_url
            fixed += 1

print(f'\nFixed: {fixed}')
with open('data/logos.json', 'w', encoding='utf-8') as f:
    json.dump(logos, f, indent=2, ensure_ascii=False)
