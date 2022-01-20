""" script: update pages name """
import json
from pathlib import Path

from OfficialTool import get_all_pages


def main():
    """ save all page name """
    pages = get_all_pages()

    all_page_file = Path("../data/all_page.json")
    json_text = json.dumps(pages, indent=4, ensure_ascii=False)
    all_page_file.write_text(json_text, encoding="UTF8")


if __name__ == '__main__':
    main()
