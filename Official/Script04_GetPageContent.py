""" get page content, check page is empty or redirect """
import json
from pathlib import Path

from Official.OfficialTool import get_session, api_url
from tools import load_json

out_path = Path("../data/page_content")
out_path.mkdir(exist_ok=True)


def main():
    """ main func
        compare last modify date for page en-zh
    """

    # json demo : [{'pageid': 123, 'ns': 0, 'title': 'Asd/zh'}, ...]

    en_pages = load_json("../data/en_pages.json")


    session = get_session()

    for i, page in enumerate(en_pages):

        title: str = page["title"]
        pageid: str = str(page["pageid"])

        print(f"{i}/{len(en_pages)} getting page: ", title, pageid)
        save_page(pageid, session)


def save_page(pageid, session=None):
    if session is None:
        session = get_session()

    req = session.get(api_url, params={
        'format': 'json',
        'action': 'query',
        'prop': 'revisions',
        'rvlimit': 1,
        'rvprop': 'ids|timestamp|flags|comment|user|userid|content',
        'pageids': pageid
    })
    data = req.json()
    revision = data["query"]["pages"][pageid]["revisions"][0]
    revision_text = json.dumps(revision, ensure_ascii=False, indent=4)
    out_file = out_path / f"{pageid}.json"
    out_file.write_text(revision_text, encoding="UTF8")


if __name__ == '__main__':
    main()
