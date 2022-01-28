from tool.wiki import get_bili_tool


def main():
    """ main func """
    target_name = "算术运算器"

    wiki = get_bili_tool()

    data = wiki.page_info_by_title(target_name, use_cache=False)

    print(data)


if __name__ == '__main__':
    main()
