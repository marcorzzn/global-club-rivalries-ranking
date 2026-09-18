import os

try:
    from PIL import Image
except ImportError:
    print("La libreria Pillow non è installata. Esegui: pip install Pillow")
    exit()

def normalize_logos(input_dir="assets/logos", output_dir="assets/logos_normalized", target_size=500):
    """
    Legge tutti i loghi scaricati, li pulisce e li normalizza creando asset
    immediatamente pronti per l'uso grafico (Figma, Canva, Photoshop).
    """
    if not os.path.exists(input_dir):
        print(f"Errore: La cartella {input_dir} non esiste. Esegui prima asset_exporter.py.")
        return
        
    os.makedirs(output_dir, exist_ok=True)
    files = os.listdir(input_dir)
    print(f"Inizio normalizzazione grafica di {len(files)} file...\n")
    
    import shutil

    for filename in files:
        filepath = os.path.join(input_dir, filename)
        outpath = os.path.join(output_dir, filename)
        
        # Gli SVG sono vettoriali: non perdono qualità e non vanno rasterizzati per sbaglio.
        # Li copiamo intatti nella cartella finale.
        if filename.lower().endswith('.svg'):
            shutil.copy2(filepath, outpath)
            print(f"[SVG Vettoriale] Copiato intatto: {filename}")
            continue
            
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
            
        try:
            with Image.open(filepath) as img:
                # Forza il convert in formato con canale Alpha (trasparenza)
                img = img.convert("RGBA")
                
                # 1. CROP: Calcola il perimetro esatto del logo ignorando i pixel trasparenti morti (bounding box)
                bbox = img.getbbox()
                if bbox:
                    img = img.crop(bbox)
                
                # 2. RIDIMENSIONAMENTO PROPORZIONALE: Scala l'immagine in modo che il lato più lungo sia esattamente 'target_size'
                img_ratio = img.width / img.height
                if img_ratio > 1:
                    new_w = target_size
                    new_h = int(target_size / img_ratio)
                else:
                    new_h = target_size
                    new_w = int(target_size * img_ratio)
                    
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                
                # 3. NORMALIZZAZIONE CANVAS: Crea uno sfondo trasparente quadrato perfetto (es. 500x500px)
                final_canvas = Image.new("RGBA", (target_size, target_size), (255, 255, 255, 0))
                
                # 4. CENTRATURA: Incolla matematicamente al centro il logo
                x_offset = (target_size - new_w) // 2
                y_offset = (target_size - new_h) // 2
                
                # Usiamo img stessa come maschera per incollare solo i pixel visibili
                final_canvas.paste(img, (x_offset, y_offset), img) 
                
                # Cambiamo l'estensione forzatamente in PNG per mantenere la trasparenza se in origine era un JPG strano
                outpath = os.path.splitext(outpath)[0] + '.png'
                final_canvas.save(outpath, "PNG")
                print(f"[PNG Normalizzato] Centrato e scalato a {target_size}x{target_size}px: {os.path.basename(outpath)}")
                
        except Exception as e:
            print(f"[!] Errore nell'elaborazione grafica di {filename}: {e}")

    print("\n--- Elaborazione Grafica Completata ---")
    print(f"I tuoi asset perfetti per il post su X.com si trovano in: '{output_dir}'")

if __name__ == "__main__":
    normalize_logos()
