""" compare page history """
import json
from pathlib import Path

from tools import load_json


def main():
    """ main func
        compare last modify date for page en-zh
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

        if zh_name in zh_page_dict:
            zh_page_id = zh_page_dict[zh_name]

            en_page_info = load_json(page_history_folder / f"{en_page_id}.json")
            zh_page_info = load_json(page_history_folder / f"{zh_page_id}.json")
            print(json.dumps(en_page_info))
            print(json.dumps(zh_page_info))

            print(en_page_info["revisions"][0]["timestamp"])
            print(zh_page_info["revisions"][0]["timestamp"])

            # isoformat 2019-11-07T12:43:07Z

            print(zh_name, )
            # get last update time
            exit(0)

            # find is need update?

        else:
            print(zh_name, "Not found===============================")





if __name__ == '__main__':
    main()
