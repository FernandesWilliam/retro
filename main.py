from github_action_parser import parse, inter_dependency_parsing
from argparse import ArgumentParser

from src.detector import Detector
from src.downloader import Downloader
from src.const import *

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
    parser.add_argument("git_urls", nargs="+")
    args = parser.parse_args()

    # Download the projects to analyse
    Downloader(args.git_urls).download()

    # Fetch their name and actions
    projects = Detector().detect()

    logger.info('Projects: %s' % ', '.join(projects.keys()))
    for project, action_files in projects.items():
        logger.info('Project %s - %s' % (project, ', '.join(action_files)))

    filename = '%s/%s/%s/%s' % (TMP_DIR, 'audacity', GITHUB_ACTION_PATH, 'build.yml')
    # up_down??
    parse(filename, [("up_down", inter_dependency_parsing)])

    filename = '%s%s/%s%s' % (TMP_DIR, 'juiceshop', GITHUB_ACTION_PATH, 'ci.yml')
    # up_down??
    parse(filename, [("up_down", inter_dependency_parsing)])

    logger.info("Parsing done !")


if __name__ == "__main__":
    main()
