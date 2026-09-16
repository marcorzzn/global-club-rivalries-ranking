import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

match = re.search(r'const RIVALRIES = (\[[\s\S]*?\]);\n// --- I18N', html)
if not match:
    match = re.search(r'const RIVALRIES = (\[[\s\S]*?\]);\n// === RIVALRY DATA END ===', html)

js_data = match.group(1)
with open('temp_extract.js', 'w', encoding='utf-8') as f:
    f.write('const fs = require("fs");\n')
    f.write('const data = ' + js_data + ';\n')
    f.write('fs.writeFileSync("data/raw_rivalries.json", JSON.stringify(data, null, 2), "utf8");\n')
