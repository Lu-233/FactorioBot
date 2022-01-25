""" compare page history """
import csv
from pathlib import Path
from dateutil.parser import isoparse

from tools import load_json


def main():
    """ main func
        compare last modify date for page en-zh

    """

    # json demo : [{'pageid': 123, 'ns': 0, 'title': 'Asd/zh'}, ...]

    zh_pages = load_json("../data/zh_pages.json")
    en_pages = load_json("../data/en_pages.json")
    page_history_folder = Path("../data/page_history")
    page_content_folder = Path("../data/page_content")

    out_csv = "../data/FactorioPageList.csv"


    try:
        exclude_pages = load_json("../data/exclude_page_list.json")
    except Exception:
        print("Can not find redirect_page_list file.")
        exclude_pages = []

    zh_page_dict = {x["title"]: x["pageid"] for x in zh_pages}
    en_page_dict = {x["title"]: x["pageid"] for x in en_pages}
    en_page_names = [x["title"] for x in en_pages]

    result_list = []
    result_list2 = []

    for en_name in en_page_names:

        # skip other language page
        if not en_name[0].encode().isalpha():
            continue

        en_page_id = str(en_page_dict[en_name])

        # skip redirect pages
        if en_page_id in exclude_pages:
            continue

        zh_name = en_name + "/zh"

        en_page_info = load_json(page_history_folder / f"{en_page_id}.json")
        en_page_content = load_json(page_content_folder / f"{en_page_id}.json")
        en_datetime = en_page_info["revisions"][0]["timestamp"]
        en_datetime = isoparse(en_datetime)

        zh_datetime = ""
        if zh_name in zh_page_dict:
            zh_page_id = zh_page_dict[zh_name]

            zh_page_info = load_json(page_history_folder / f"{zh_page_id}.json")
            zh_datetime = zh_page_info["revisions"][0]["timestamp"]
            zh_datetime = isoparse(zh_datetime)

            result_list.append([en_name,
                                str(en_datetime).replace('+00:00', ''),
                                len(en_page_content['*']),
                                zh_name,
                                str(zh_datetime).replace('+00:00', ''),
                                (en_datetime > zh_datetime) if zh_datetime else 'True',
                                ])
        else:
            result_list2.append([en_name,
                                str(en_datetime).replace('+00:00', ''),
                                len(en_page_content['*']),
                                zh_name,
                                str(zh_datetime).replace('+00:00', ''),
                                (en_datetime > zh_datetime) if zh_datetime else 'True',
                                ])

    with open(out_csv, "w", encoding="UTF8") as f:
        write = csv.writer(f)
        write.writerow(["en_name", "en_time", "en_len", "zh_name", "zh_time", "need_update"])
        write.writerows(result_list)
        write.writerows(result_list2)


if __name__ == '__main__':
    main()
