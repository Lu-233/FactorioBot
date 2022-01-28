""" script: get all pages name """
from tool.wiki import get_official_tool as get_tool


def main():
    """ save all page name """

    wiki = get_tool()

    all_page = wiki.pages(use_cache=True)

    for page in all_page:
        print(page)


if __name__ == '__main__':
    main()
