""" get page content, check page is empty or redirect """
import json
from pathlib import Path

from tools import load_json


def main():
    """ main func
        compare last modify date for page en-zh
    """

    # json demo : [{'pageid': 123, 'ns': 0, 'title': 'Asd/zh'}, ...]

    en_pages = load_json("../data/en_pages.json")

    content_path = Path("../data/page_content")

    redirect_list_file = Path("../data/redirect_page_list.json")

    redirect_page_ids = []

    for i, page in enumerate(en_pages):

        title: str = page["title"]
        pageid: str = str(page["pageid"])

        # skip other language page
        if not title[0].encode().isalpha():
            continue

        # print(f"{i}/{len(en_pages)} getting page: ", title, pageid)

        content_file = content_path / f"{pageid}.json"

        text = content_file.read_text("UTF8")
        page_data = json.loads(text)
        content: str = page_data["*"]

        if content.startswith("#REDIRECT"):
            redirect_page_ids.append(pageid)

    redirect_list_file.write_text(json.dumps(redirect_page_ids), encoding="UTF8")


if __name__ == '__main__':
    main()
