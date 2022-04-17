import json
from configparser import ConfigParser
from typing import Dict
import pathlib

import yaml


def ini_to_dict(ini_path: str) -> Dict:
    """Convert an INI file to a dictionary."""
    config = ConfigParser()
    config.read(ini_path)
    return {section: dict(config.items(section)) for section in config.sections()}


def json_to_dict(json_path: str) -> Dict:
    return json.loads(json_path)


def yaml_to_dict(yaml_path: str) -> Dict:
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)


def detect_config(directory: str):
    dir_contents = list(pathlib.Path(directory).iterdir())
    for f in dir_contents:
        if f.suffix == ".yaml":  # Always prioritize .yaml files
            return (f, yaml_to_dict(f))
        elif f.suffix == ".ini":
            return (f, ini_to_dict(f))
        elif f.suffix == ".json":
            return (f, json_to_dict(f))
        else:
            raise ValueError(f"Unsupported file type:  {f}")
        


if __name__ == "__main__":
    print(detect_config("./"))