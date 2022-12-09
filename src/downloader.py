from src.const import TMP_DIR, GITHUB_ACTION_PATH
import logging
import requests
from abc import ABC, abstractmethod
from src.model import RunConfig, _Project
from os.path import exists
from os import mkdir


class Downloader(ABC):
    @abstractmethod
    def download(self, output_path: str = TMP_DIR):
        pass


class FileDownloader(Downloader):
    def __init__(self, run_config: RunConfig):
        self.__projects = run_config['projects']
        self.logger = logging.getLogger(Downloader.__name__)
        self.__action_path = GITHUB_ACTION_PATH

    def __download_file(self, url: str, dest: str):
        """Download a file and put it at a specified destination"""
        try:
            if exists(dest):
                self.logger.info("File %s already exists, no need to download it again.", dest)
                return

            self.logger.debug('Downloading file %s from %s' % (dest, url))
            content = requests.get(url).text

            if not content:
                self.logger.warning('Content not found for %s (from %s)' % (dest, url))
                return

            with open(dest, 'w+') as cout:
                cout.write(content)
            self.logger.debug('Download complete for file %s' % dest)
        except IOError as e:
            self.logger.warning('Got an exception trying to write file %s: %s' % (dest, e.__str__()))

    @staticmethod
    def __get_url_for_file(repository: str, branch: str, file: str):
        """Build a download url for a GitHub file"""
        return 'https://raw.github.com/' + repository.replace('https://github.com', '') + '/' + branch + '/' + file

    def __download_artifacts_from_repository(self, projectname: str, repository: _Project, output_path: str):
        """Download files for a GitHub project"""
        self.logger.debug('Repository %s: %s' % (projectname, repository))
        if not exists(output_path + '/' + projectname):
            mkdir(output_path + '/' + projectname)
        for action in repository['actions']:
            output = output_path + '/' + projectname + '/' + action['name']
            url = self.__get_url_for_file(repository['git_url'], repository['branch'], self.__action_path + action['name'])
            self.__download_file(url, output)

    def download(self, output_path: str = TMP_DIR):
        """Download git repository"""
        for projectname, _project in self.__projects.items():
            self.__download_artifacts_from_repository(projectname, _project, output_path)
