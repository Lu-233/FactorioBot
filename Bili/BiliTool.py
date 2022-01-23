"""
    bili wiki bot

    thanks https://github.com/YorkSu/bwt
"""

from Bili.bili_session import login_bili_wiki

url = f"https://wiki.biligame.com/factorio/api.php"


def main():
    """ main for test """

    session = login_bili_wiki(browser_name="Edge", wiki_name="factorio")




if __name__ == '__main__':
    main()
