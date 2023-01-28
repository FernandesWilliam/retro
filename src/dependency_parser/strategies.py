from abc import ABC, abstractmethod


class InterScanStrategy(ABC):
    @abstractmethod
    def parse(self, jobs: dict, graph: dict):
        pass


class IntraScanStrategy(ABC):
    @abstractmethod
    def parse(self, job: dict, graph: dict):
        pass
