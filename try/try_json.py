import json
from pathlib import Path


all_page_text = Path("../data/all_page.json").read_text("UTF8")
pages = json.loads(all_page_text)

for x in pages:
    print(x["title"])