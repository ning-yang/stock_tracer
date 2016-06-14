import yaml
import inspect
from os import path

CONFIG_DIRECTORY = "config"

def get_configuration(config_name, missing_ok=False):
    """get_configuration get configurations from specific configuration file

    :param config_name: Configuration file name.
    :param missing_ok: Whether it is OK if the configuration file doesn't exist.
    """
    assert config_name

    current_file_path = inspect.getfile(inspect.currentframe())
    current_proejct_root = path.dirname(path.dirname(path.abspath(current_file_path)))
    config_folder_path = path.join(current_proejct_root, CONFIG_DIRECTORY)

    patterns = ["", ".yaml", ".yml", ".conf"]
    for pattern in patterns:
        config_file = path.join(config_folder_path, config_name + pattern)
        if path.isfile(config_file):
            break
    else:
        if missing_ok:
            return {}
        else:
            raise Exception("Configuration file {0} is not found under {1}".format(config_name, config_folder_path))

    with open(config_file, "r") as yaml_file:
        config = yaml.load(yaml_file.read())

    return config if config else {}
