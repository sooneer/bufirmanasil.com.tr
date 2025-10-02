import json
import re

# Dosyayı oku
with open('public/data/SektorKodlari.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# JSON'u parse et
data = json.loads(content)

# Basit format için liste oluştur
sector_list = []

for item in data['data']['parameterItems']:
    code = item['prmName']
    # Türkçe açıklamayı bul
    name = ""
    for i18n_item in item['i18N']['i18NContentList']:
        if i18n_item['language'] == 'tr':
            name = i18n_item['i18NText']
            break

    if code and name:
        sector_list.append({
            "code": code,
            "name": name
        })

# Koda göre sırala
sector_list.sort(key=lambda x: x['code'])

# Yeni JSON dosyasına yaz
output_data = {
    "sectors": sector_list
}

with open('public/data/SektorKodlari.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"Toplam {len(sector_list)} sektör kodu dönüştürüldü.")
print("Dosya 'public/data/SektorKodlari.json' olarak kaydedildi.")
