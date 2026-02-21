import os
import json

folder_path = r"C:\Users\moste\Downloads\CREA_total"
output_file = r"C:\Users\moste\OneDrive\Documents\VS studio goed\spaans_afrikaans_engels.json"

vocabulary = []
limit = 500  # stoor net die eerste 500 woorde vir toets
count = 0

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding="latin-1", errors="ignore") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3 and not parts[0].isdigit():
                    spanish = parts[0]
                    try:
                        freq_abs = int(parts[1].replace(",", ""))
                    except ValueError:
                        freq_abs = None
                    try:
                        freq_norm = float(parts[2])
                    except ValueError:
                        freq_norm = None

                    vocabulary.append({
                        "spanish": spanish,
                        "afrikaans": ["(nog nie vertaal nie)"],
                        "english": ["(not yet translated)"],
                        "frequency": freq_abs,
                        "normalized": freq_norm
                    })

                    count += 1
                    if count >= limit:
                        break
        if count >= limit:
            break

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(vocabulary, f, ensure_ascii=False, indent=2)

print(f"Laai klaar: {len(vocabulary)} woorde gestoor in {output_file}")
