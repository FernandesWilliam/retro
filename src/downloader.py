from src.const import TMP_DIR, GITHUB_ACTION_PATH
import logging
import requests
from abc import ABC, abstractmethod
from src.model import RunConfig, _Project
from os.path import exists
from os import mkdir
from git import Repo


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


class RepoDownloader(Downloader):
    """Download a repository git"""
    def __init__(self, run_config: RunConfig):
        self.__projects = {name: project['git_url'] for name, project in run_config['projects'].items()}
        self.logger = logging.getLogger(Downloader.__name__)

    def __download_repo(self, repo_name, repo_url, output_path):
        """Download a git repository to the output directory"""
        # Assert that the url is a git clone url
        if exists(output_path + repo_name):
            self.logger.info("Repo %s already exists, no need to download it again.", output_path + repo_name)
            return

        if '.git' not in repo_url:
            repo_url += '.git'
        self.logger.info("Downloading %s to %s" % (repo_url, output_path + repo_name))
        Repo.clone_from(repo_url, output_path + repo_name)
        self.logger.debug('Downloading of %s done !' % repo_name)

    def download(self, output_path: str = TMP_DIR):
        """Download git repository"""
        for name, url in self.__projects.items():
            self.__download_repo(name, url, output_path)
