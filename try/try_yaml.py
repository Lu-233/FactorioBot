""" test """
from pathlib import Path

import yaml


def main():
    """ main func """
    print("hello factorio")

    data = {
        'wiki': {
            'foo': 'bar',
            'key': 'value',
            'the answer': 42
        },
        'bili_wiki': {
            'foo': 'bar',
            'key': 'value',
            'the answer': 42
        }
    }

    cfg_file = Path("key_test.yaml")
    # Write YAML file
    with cfg_file.open('w+', encoding='utf8') as outfile:
        yaml.safe_dump(data, outfile, default_flow_style=False, allow_unicode=True)

    # Read YAML file
    data_loaded = yaml.safe_load(cfg_file.read_text(encoding="UTF8"))

    print(data)
    print(data_loaded)
    print(data == data_loaded)


if __name__ == '__main__':
    main()
