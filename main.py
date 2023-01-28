from argparse import ArgumentParser

from src.model import RunConfig
from src.parser import yaml_parse
from src.downloader import Downloader
from src.dependency_parser.scanner import Scanner
from src.const import *
from os.path import exists

from src.dependency_parser.dependency_grapher import make_graph
from src.graph_builder import DotGraphBuilder
import logging
import logging.config
import os


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

    logger.debug("Run configuration: %s" % run_config)
    already_download = lambda project: exists(f"{TMP_DIR}/{project}/{GITHUB_ACTION_PATH}")

    # Download the projects to analyse
    Downloader([run_config['projects'][name]['git_url'] for name in run_config['projects'] if
                not already_download(name)]).download()

    # Parse actions from the projects
    for project, data in run_config['projects'].items():
        scanner = Scanner(
            project,
            f"{TMP_DIR}/{project}",
            actions = data['actions'] if 'actions' in data else []
        )
        scanner.parse()

        graphs = scanner.get_graph()

        try:
            os.makedirs(f'results/{project}')
        except FileExistsError: # Avoid error if directory already created
            pass

        for name, graph in graphs.items():
            DotGraphBuilder(graph).generate(name, output_dir = f'results/{project}')

    logger.info("Parsing done !")


if __name__ == "__main__":
    main()
