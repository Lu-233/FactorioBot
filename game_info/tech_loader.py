"""
    load game data
    use lupa run lua code, load factorio data
"""
import configparser
import pickle
from collections import OrderedDict
from pathlib import Path
from lupa import LuaRuntime

def main():
    # base_cfg = load_base_cfg()
    # print(base_cfg.sections())
    # # technology-name  technology-description
    # for k, v in base_cfg["technology-description"].items():
    #     print(k, "\t", k in base_cfg["technology-name"])
    # for k, v in base_cfg["item-name"].items():
    #     print(k, "\t", v)
    # for k, v in base_cfg["item-description"].items():
    #     print(k, "\t", v)
    # for k, v in base_cfg["item-limitation"].items():
    #     print(k, "\t", v)

    # data = load_item(ver="1.1.53")
    # print(data["solid-fuel-from-heavy-oil"])
    # for k,v in data.items():
    #     print(k, v)

    pass



def remove_num_tail(name: str):
    names = name.split("-")
    if names[-1].isnumeric():
        return name.replace(f"-{names[-1]}", "")
    return name


def load_base_cfg():
    config = configparser.ConfigParser()
    config.read('trans/base.cfg', "UTF8")
    return config


def load_tech(ver="1.1.53", use_cache=True) -> OrderedDict:
    tech_cache = Path(f"game_data/{ver}.technology")

    if use_cache and tech_cache.exists():
        data: OrderedDict = pickle.loads(tech_cache.read_bytes())
        return data

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
    data = OrderedDict(sorted(table2dict(data).items()))

    tech_cache.write_bytes(pickle.dumps(data))

    return data


def load_item(ver="1.1.53", use_cache=True) -> OrderedDict:
    tech_cache = Path(f"game_data/{ver}.item")

    if use_cache and tech_cache.exists():
        data: OrderedDict = pickle.loads(tech_cache.read_bytes())
        return data

    lua = LuaRuntime()

    folder = ver.replace(".", "/")

    # like require "game_data/1/1/53/technology"
    get_data = lua.eval(f"""
                    function()
                        require "game_data/{folder}/dataloader"
                        require "game_data/{folder}/util"
                        require "game_data/{folder}/item"
                        return data
                    end
                """)
    data: dict = get_data()["raw"]["item"]
    data = OrderedDict(sorted(table2dict(data).items()))

    tech_cache.write_bytes(pickle.dumps(data))

    return data


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

    return dict(data)


if __name__ == '__main__':
    main()
    pass
