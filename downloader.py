import os.path

from git import Repo


class Downloader:
    def __init__(self, repository_path: str):
        if '.git' not in repository_path:
            print("Given path is not a valid git url")
            exit(1)
        self.__git_url = repository_path

    def download(self, output_path: str = 'output/'):
        repo_name = self.__git_url.split(os.path.sep)[-1]
        print("Downloading %s to %s" % (self.__git_url, output_path + repo_name[:-len('.git')]))
        Repo.clone_from(self.__git_url, output_path + repo_name[:-len('.git')])
