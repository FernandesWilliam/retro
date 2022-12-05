import yaml


def yaml_parse(filename):
    """Parse a yaml file"""
    with open(filename, "r") as cin:
        return yaml.safe_load(cin)