"""
    load game data
    use lupa run lua code, load factorio data
"""
import configparser
from collections import OrderedDict

from lupa import LuaRuntime


def remove_num_tail(name: str):
    names = name.split("-")
    if names[-1].isnumeric():
        return name.replace(f"-{names[-1]}", "")
    return name


def load_trans():
    config = configparser.ConfigParser()
    config.read('trans/base.cfg', "UTF8")
    return config


def load_tech(ver="1.1.53"):
    lua = LuaRuntime()

    folder = ver.replace(".", "/")

    # like require "game_data/1/1/53/technology"
    get_data = lua.eval(f"""
                    function()
                        require "game_data/{folder}/dataloader"
                        require "game_data/{folder}/util"
                        require "game_data/{folder}/technology"
                        return data
                    end
                """)
    data: dict = get_data()["raw"]["technology"]

    return table2dict(data)


def table2dict(data):
    """ lupa._lupa._LuaTable to dict """
    if str(type(data)) != "<class 'lupa._lupa._LuaTable'>":
        return data
    for k, v in data.items():
        if str(type(v)) != "<class 'lupa._lupa._LuaTable'>":
            continue
        if 1 in list(v.keys()):
            if k == "ingredients":
                data[k] = {y[1]: y[2] for x, y in v.items()}
            else:
                data[k] = [table2dict(y) for x, y in v.items()]
        else:
            data[k] = table2dict(v)

    return OrderedDict(sorted(dict(data).items()))


if __name__ == '__main__':
    main()
