import json
from typing import Dict
import pathlib

import yaml


def json_to_dict(json_path: str) -> Dict:
    return json.loads(json_path)


def yaml_to_dict(yaml_path: str) -> Dict:
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)


def detect_config(directory: str):
    dir_contents = list(pathlib.Path(directory).iterdir())
    for f in dir_contents:
        if (
            f.suffix == ".json"
        ):  # In my opinion, .json is the most common config file, so chances are people will now it's syntax.
            return (f, json_to_dict(f))
        if (
            f.suffix == ".yaml"
        ):  # .yaml is a common config file, but not the most common.
            return (f, yaml_to_dict(f))
    return None


if __name__ == "__main__":
    print(detect_config("./"))
