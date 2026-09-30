import urllib.request
import json
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
url = f"https://jidelnicek.utb.cz/webkredit/Api/Ordering/ExportMenu?canteenId=2&dates={today}T00:00:00.000Z&locale=cs"

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0'}
)

try:
    with urllib.request.urlopen(req) as response:
        if response.status == 200:
            data = json.loads(response.read().decode('utf-8'))
            with open('menu.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("Menu successfully saved to menu.json")
except Exception as e:
    print(f"Error fetching menu: {e}")
