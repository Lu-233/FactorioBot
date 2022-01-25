""" get page content, check page is empty or redirect, or exclude """
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

    exclude_list_file = Path("../data/exclude_page_list.json")

    exclude_page_ids = []

    for i, page in enumerate(en_pages):

        title: str = page["title"]
        pageid: str = str(page["pageid"])

        # skip other language page
        if not title[0].encode().isalpha():
            continue

        # base on wiki rule, page start with Prototype should not be translate
        if title.startswith("Prototype"):
            exclude_page_ids.append(pageid)

        # print(f"{i}/{len(en_pages)} getting page: ", title, pageid)

        content_file = content_path / f"{pageid}.json"

        text = content_file.read_text("UTF8")
        page_data = json.loads(text)
        content: str = page_data["*"]

        # for redirect page
        if content.startswith("#REDIRECT"):
            exclude_page_ids.append(pageid)

        # for archive page
        if content.find("{{archive}}") > 0:
            exclude_page_ids.append(pageid)

        # for Technical page, not need trans
        if content.find("[[Category:Technical]]") > 0:
            exclude_page_ids.append(pageid)

    exclude_list_file.write_text(json.dumps(exclude_page_ids, indent=4), encoding="UTF8")


if __name__ == '__main__':
    main()
