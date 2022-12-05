# from github_action_parser import parse, inter_dependency_parsing
from argparse import ArgumentParser

from src.detector import Detector
from src.downloader import Downloader

import logging
import logging.config

# parse("./repositories/audacity/build.yml", [
#     ("up_down", inter_dependency_parsing)
#
#     ])
#
#
# parse("./repositories/juicyshop/ci.yml", [
#     ("up_down", inter_dependency_parsing)
#
#     ])


def setup_logging():
    """Set up the logging using the configuration file"""
    logging.config.fileConfig('config/logging.conf')


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    parser = ArgumentParser(prog="GitHub Action Analyser")

    parser.add_argument("git_urls", nargs="+")

    args = parser.parse_args()

    Downloader(args.git_urls).download()

    projects = Detector().detect()

    logger.info('Projects: %s' % ', '.join(projects.keys()))

    for project, action_files in projects.items():
        logger.info('Project %s - %s' % (project, ', '.join(action_files)))


if __name__ == "__main__":
    main()
