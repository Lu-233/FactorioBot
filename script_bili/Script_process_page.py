""" script: get all pages name """
import pandas as pd

from script_bili.S01_UpdateWantedPage import need_edit
from tool.wiki import get_bili_tool as get_tool


def main():
    wiki = get_tool()

    pages = wiki.get_wanted_pages(use_cache=True)

    filtered = [p for p in pages if need_edit(wiki, p)]

    for page in filtered:
        page["category"] = "未知"
        page["reason"] = f"由Wiki API计算，请参考[[https://wiki.biligame.com/factorio/index.php?title=特殊:链入页面&target={page['title']}|链入页面]]"
        print(page)

    # print(len(wiki.get_inlink(page["title"])))
    # https://wiki.biligame.com/factorio/index.php?title=特殊:链入页面&target=蜘蛛遥控器


def filter_wanted_page(pages):
    filtered = []
    for page in pages:

        if int(page["value"]) <= 1:
            continue

        title: str = page["title"]

        filtered.append(page)

    return filtered


def page2excel():
    """ save all page name """

    wiki = get_tool()

    all_pages = wiki.pages(use_cache=True)

    excel_file = "test.xlsx"
    writer = pd.ExcelWriter(str(excel_file), engine='xlsxwriter')
    df = pd.DataFrame(all_pages)
    print(df)
    df.to_excel(writer, sheet_name="a", index=False)
    writer.save()


if __name__ == '__main__':
    main()
