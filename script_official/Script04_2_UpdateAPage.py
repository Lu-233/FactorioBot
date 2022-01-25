from tool.wiki import get_official_tool


def main():
    """ main func """
    target_name = "Acid"

    wiki = get_official_tool()

    data = wiki.page_info_by_title(target_name, use_cache=False)

    print(data)


if __name__ == '__main__':
    main()
