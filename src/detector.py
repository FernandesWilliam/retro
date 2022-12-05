from src.const import *
import os


class Detector:
    def __init__(self, path: str = TMP_DIR, actions_path: str = GITHUB_ACTION_PATH):
        self.__path = path
        self.__actions_path = actions_path

    def __get_project_names(self) -> list[str]:
        """Find out the projects to analyse"""
        with os.scandir(self.__path) as source_dir:
            return [entry.name for entry in source_dir if not entry.name.startswith('.') and not entry.is_file()]

    def __get_action_file(self, project: str) -> list[str]:
        """Find out the actions declared for a project"""
        path: str = '%s/%s/%s' % (self.__path, project, self.__actions_path)
        with os.scandir(path) as action_dir:
            return [
                entry.name
                for entry in action_dir
                if entry.is_file() and (entry.name.endswith('.yml') or entry.name.endswith('.yaml'))
            ]

    def detect(self) -> dict[str, list[str]]:
        """Detects the projects and their actions"""
        if not os.path.exists(self.__path):
            return {}
        return {name: self.__get_action_file(name) for name in self.__get_project_names()}
