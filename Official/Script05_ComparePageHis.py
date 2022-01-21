""" compare page history """
import json
from pathlib import Path
from dateutil.parser import isoparse

from tools import load_json


def main():
    """ main func
        compare last modify date for page en-zh

        the output can be handly save to csv file
    """

    # json demo : [{'pageid': 123, 'ns': 0, 'title': 'Asd/zh'}, ...]

    zh_pages = load_json("../data/zh_pages.json")
    en_pages = load_json("../data/en_pages.json")
    page_history_folder = Path("../data/page_history")


    try:
        redirect_pages = load_json("../data/redirect_page_list.json")
    except Exception:
        print("Can not find redirect_page_list file.")
        redirect_pages = []

    zh_page_dict = {x["title"]: x["pageid"] for x in zh_pages}
    en_page_dict = {x["title"]: x["pageid"] for x in en_pages}
    zh_page_names = [x["title"] for x in zh_pages]
    en_page_names = [x["title"] for x in en_pages]

    for en_name in en_page_names:

        # skip other language page
        if not en_name[0].encode().isalpha():
            continue

        en_page_id = str(en_page_dict[en_name])

        # skip redirect pages
        if en_page_id in redirect_pages:
            continue

        zh_name = en_name + "/zh"

        en_page_info = load_json(page_history_folder / f"{en_page_id}.json")
        en_datetime = en_page_info["revisions"][0]["timestamp"]
        en_datetime = isoparse(en_datetime)

        zh_datetime = ""
        if zh_name in zh_page_dict:
            zh_page_id = zh_page_dict[zh_name]

            zh_page_info = load_json(page_history_folder / f"{zh_page_id}.json")
            zh_datetime = zh_page_info["revisions"][0]["timestamp"]
            zh_datetime = isoparse(zh_datetime)

        print(f"{en_name}\t"
              f"{zh_name}\t"
              f"{str(en_datetime).replace('+00:00', '')}\t"
              f"{str(zh_datetime).replace('+00:00', '')}\t"
              f"{(en_datetime > zh_datetime) if zh_datetime else 'True'}\t"
              )

if __name__ == '__main__':
    main()
