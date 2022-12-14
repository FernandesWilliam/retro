"""The classes below are there to ensure that the minimum information is given as input to the program."""
from typing import TypedDict


class _Action(TypedDict):
    """An action is defined by the name of the file where it is declared and by the parsers to be used during the
    analysis. """
    name: str
    parsers: list[str]


class _Project(TypedDict):
    """A project is defined by a URL from which to download files, a branch and a set of actions to analyse."""
    git_url: str
    branch: str
    actions: list[_Action]


class RunConfig(TypedDict):
    """The runtime configuration is just a dictionary of the projects to be analysed referenced by name."""
    projects: dict[str, _Project]
