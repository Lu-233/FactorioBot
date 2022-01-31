import json
from pathlib import Path


def load_json(filepath):
    """ read json from file """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Can not find file: {filepath}.")

    text = filepath.read_text("UTF8")
    data = json.loads(text)
    return data
