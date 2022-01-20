""" cfg tools """
import yaml
from pathlib import Path

cfg_file = r"../key.yaml"


def load_cfg() -> dict:
    """ load yaml cfg """
    yaml_text = Path(cfg_file).read_text(encoding="UTF8")
    cfg = yaml.safe_load(yaml_text)
    return cfg
