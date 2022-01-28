""" script: get all pages name """

from tool.wiki import get_official_tool as get_tool


def main():
    """ save all page name """

    wiki = get_tool()

    en_pages = wiki.pages_lang(lang='en')

    for page in en_pages:
        if not need_edit(page):
            continue
        content = wiki.page_info(page_id=page["pageid"])["*"]
        if not need_edit_content(content):
            continue

        page_type = "article"
        if content.find(":Infobox:") > 0:
            page_type = "item"

        print(page["title"], "\t", page_type, "\t", count_words(content))


def need_edit_content(content: str):
    """ check need edit by content """
    # skip REDIRECT page
    if content.startswith("#REDIRECT"):
        return False

    # skip disambiguation page
    if content.find("{{Disambiguation}}") > -1:
        return False
    if content.find("{{disambiguation}}") > -1:
        return False

    return True


def need_edit(page: dict):
    """ check need edit by title """
    title: str = page["title"]
    if title.startswith("Prototype"):
        return False
    if title.startswith("Types"):
        return False
    if title.find("(research)") > -1:
        return False

    return True


def count_words(content: str):
    """ dirty code for count word """
    content = content.replace("{{Languages}}", "")
    content = content.replace("\n", " ")
    content = content.replace("'", " ")
    content = content.replace("[", " ")
    content = content.replace("]", " ")
    content = content.replace("=", " ")
    content = content.replace(">", " ")
    content = content.replace("<", " ")
    content = content.replace("{", " ")
    content = content.replace("}", " ")
    content = content.replace("|", " ")
    content = content.replace("(", " ")
    content = content.replace(")", " ")
    content = content.replace("*", " ")
    content = content.replace(":", " ")
    content = content.replace("-", " ")
    content = content.replace("!", " ")
    content = content.replace("\"", " ")
    content = content.replace("#", " ")
    content = content.replace("_", " ")
    content = content.replace("+", " ")
    content = content.replace("/", " ")
    content = content.replace(".", " ")
    content = content.replace("0", "")
    content = content.replace("1", "")
    content = content.replace("2", "")
    content = content.replace("3", "")
    content = content.replace("4", "")
    content = content.replace("5", "")
    content = content.replace("6", "")
    content = content.replace("7", "")
    content = content.replace("8", "")
    content = content.replace("9", "")
    content = content.replace("`", "")
    content = content.replace("&", "")
    content = content.replace("%", "")
    content = content.replace("", "")
    content = content.replace(" q ", "")
    content = content.replace(" w ", "")
    content = content.replace(" e ", "")
    content = content.replace(" r ", "")
    content = content.replace(" t ", "")
    content = content.replace(" y ", "")
    content = content.replace(" u ", "")
    content = content.replace(" i ", "")
    content = content.replace(" o ", "")
    content = content.replace(" p ", "")
    content = content.replace(" s ", "")
    content = content.replace(" d ", "")
    content = content.replace(" f ", "")
    content = content.replace(" g ", "")
    content = content.replace(" h ", "")
    content = content.replace(" j ", "")
    content = content.replace(" k ", "")
    content = content.replace(" l ", "")
    content = content.replace(" z ", "")
    content = content.replace(" x ", "")
    content = content.replace(" c ", "")
    content = content.replace(" v ", "")
    content = content.replace(" b ", "")
    content = content.replace(" n ", "")
    content = content.replace(" m ", "")

    content = content.replace("        ", " ")
    content = content.replace("     ", " ")
    content = content.replace("    ", " ")
    content = content.replace("   ", " ")
    content = content.replace("  ", " ")
    content = content.strip()
    while content.find("  ") > -1:
        content = content.replace("  ", " ")

    return len(content.split(" "))


if __name__ == '__main__':
    main()
