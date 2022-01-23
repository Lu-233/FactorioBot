""" script: update pages history """
import json
from pathlib import Path

from Official.OfficialTool import api_url, get_session
from tools import load_json

his_store = Path("../data/page_history")
his_store.mkdir(exist_ok=True)


def main():
    """ main """
    # pages = get_all_history("../data/zh_pages.json")
    get_all_history("../data/en_pages.json")
    # pages = Path("../data/en_pages.json")


def get_all_history(filepath):

    pages = load_json(filepath)
    # [{'pageid': 23, 'title': 'Acor/zh'}, ... , {'pageid': 2, 'title': 'Acts/zh'}]

    session = get_session()

    for i, page in enumerate(pages):
        print(f"{i}/{len(pages)} get history for: ", page["title"], page["pageid"])

        get_page_history(page, session)


def get_page_history(page, session=None):
    """ get history """

    if session is None:
        session = get_session()

    pageid = str(page["pageid"])

    req = session.get(api_url, params={
        'format': 'json',
        'action': 'query',
        'prop': 'revisions',
        'rvlimit': 25,
        'rvprop': 'timestamp|user|comment',
        'pageids': pageid
    })

    revisions = req.json()["query"]["pages"][pageid]["revisions"]

    revisions = {
        "page": page,
        "revisions": revisions
    }
    save = his_store / f'{page["pageid"]}.json'
    save.write_text(json.dumps(revisions, ensure_ascii=False, indent=4), encoding="UTF8")



def split(data, length):
    """ split list to list of list
        https://stackoverflow.com/questions/312443/how-do-you-split-a-list-or-iterable-into-evenly-sized-chunks
    """
    length = max(1, length)
    return (data[i:i + length] for i in range(0, len(data), length))

if __name__ == '__main__':
    main()
