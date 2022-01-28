""" get page content, check page is empty or redirect """
from tool.wiki import get_official_tool as get_tool

def main():
    """ main func
        compare last modify date for page en-zh
    """

    # json demo : [{'pageid': 123, 'ns': 0, 'title': 'Asd/zh'}, ...]

    wiki = get_tool()

    en_pages = wiki.pages_lang("en")

    for page in en_pages:
        info = wiki.page_info(page["pageid"], use_cache=True)
        print(info)
        break


if __name__ == '__main__':
    main()
