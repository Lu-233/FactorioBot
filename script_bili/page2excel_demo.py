""" script: get all pages name """
import pandas as pd

from tool.wiki import get_bili_tool as get_tool


def main():
    wiki = get_tool()

    pages = wiki.get_wanted_pages(use_cache=True)


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
