""" script: split all page to lang, new get en and zh """
import json
from pathlib import Path


def main():
    """ main """
    pages = Path("../data/all_page.json")

    if not pages.exists():
        print("Can not find ../data/all_page.json, please update page name")
        exit(0)

    pages = json.loads(pages.read_text("UTF8"))

    if len(pages) < 4000:
        print(f"page num is tooooo few ({len(pages)}), expected num is >4200")
        exit(0)

    zh_pages = [page for page in pages if page["title"].find("/zh") > 0]
    en_pages = [page for page in pages if page["title"].find("/") < 0]

    Path("../data/zh_pages.json").write_text(json.dumps(zh_pages, indent=4, ensure_ascii=False), encoding="UTF8")
    Path("../data/en_pages.json").write_text(json.dumps(en_pages, indent=4, ensure_ascii=False), encoding="UTF8")


if __name__ == '__main__':
    main()
