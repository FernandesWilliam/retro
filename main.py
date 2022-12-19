#from github_action_parser import parse, inter_dependency_parsing
from argparse import ArgumentParser

from src.model import RunConfig
from src.parser import yaml_parse
from src.downloader import Downloader, FileDownloader
from src.const import *
from os.path import exists


import os
from src.dependency_parser.dependency_grapher import make_graph
import logging
import logging.config


def setup_logging():
    """Set up the logging using the configuration file"""
    logging.config.fileConfig('config/logging.conf')


def main():
    # Set up logging and get __main__ logger
    setup_logging()
    logger = logging.getLogger(__name__)

    # Set up the arg parser and get the args
    parser = ArgumentParser(prog="GitHub Action Analyser")
    parser.add_argument("run_config")
    args = parser.parse_args()

    run_config: RunConfig = yaml_parse(args.run_config)

    logger.info("Run configuration: %s" % run_config)

    # Download the projects to analyse
    downloader: Downloader = FileDownloader(run_config)
    downloader.download()

    # Parse actions from the projects
    for project in run_config['projects']:
        for action in run_config['projects'][project]['actions']:
            filename = '%s/%s/%s' % (TMP_DIR, project, action['name'])
            logger.info('Parsing %s' % filename)
            make_graph(filename, action['parsers'])

    logger.info("Parsing done !")


if __name__ == "__main__":
    main()
