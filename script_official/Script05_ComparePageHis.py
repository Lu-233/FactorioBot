""" compare page history """
import csv
from pathlib import Path
from dateutil.parser import isoparse

from tools import load_json
from tool.wiki import get_official_tool as get_tool

def main():
    """ main func
        compare last modify date for page en-zh

    """

    # json demo : [{'pageid': 123, 'ns': 0, 'title': 'Asd/zh'}, ...]

    wiki = get_tool()

    en_pages = wiki.pages_lang("en")

    out_csv = "../data/FactorioPageList.csv"

    try:
        exclude_pages = load_json("../data/exclude_page_list.json")
    except FileNotFoundError:
        print("Can not find redirect_page_list file.")
        exclude_pages = []

    result_list = []

    for en_page in en_pages:
        en_name = en_page["title"]

        # skip other language page
        if not en_name[0].encode().isalpha():
            continue

        en_page_id = str(en_page["pageid"])

        # skip redirect pages
        if en_page_id in exclude_pages:
            continue

        en_page_info = wiki.page_info(en_page_id)
        en_page_content = en_page_info["*"]
        en_datetime = isoparse(en_page_info["timestamp"])

        zh_name = en_name + "/zh"

        try:
            zh_page_info = wiki.page_info_by_title(zh_name)
            zh_datetime = isoparse(zh_page_info["timestamp"])
        except RuntimeError:
            zh_datetime = ""

        result_list.append([en_name,
                            str(en_datetime).replace('+00:00', ''),
                            len(en_page_content),
                            zh_name,
                            str(zh_datetime).replace('+00:00', ''),
                            (en_datetime > zh_datetime) if zh_datetime else 'True',
                            ])

    with open(out_csv, "w", encoding="UTF8") as f:
        write = csv.writer(f)
        write.writerow(["en_name", "en_time", "en_len", "zh_name", "zh_time", "need_update"])
        write.writerows(result_list)


if __name__ == '__main__':
    main()
