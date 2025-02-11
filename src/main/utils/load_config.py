from configparser import ConfigParser
import os

def read_config_params(config_file_path: str) -> ConfigParser:
    """
    Reads an INI configuration file.
    
    @config_file_path: Path to the config file.
    @return: ConfigParser object with loaded configuration.
    """
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Config file '{config_file_path}' not found.")
    
    config_object = ConfigParser()
    config_object.read(config_file_path)
    
    if not config_object.sections():
        raise ValueError(f"Config file '{config_file_path}' is empty or not formatted correctly.")
    
    return config_object