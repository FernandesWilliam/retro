from src.dependency_parser.strategies import IntraScanStrategy
import os


class Strategy(IntraScanStrategy):
    __cmds = {
        'npm': 'package.json',
        'mvn': 'pom.xml'
    }

    def __init__(self, project_path):
        super().__init__(project_path)

    def parse(self, job: dict, graph: dict):
        checkout = False

        for step in job['steps']:
            if 'name' not in step:
                step['name'] = step['id'] if 'id' in step else (step['uses'] if 'uses' in step else 'Anonymous step')
            
            if step['name'] not in graph:
                graph[step['name']] = []

            # Does the step make a checkout
            if 'uses' in step and 'actions/checkout' in step['uses']:
                checkout = step['name']
            
            if 'run' in step:
                self.__check_file_usage(step['name'], step['run'], checkout, graph)
    
    def __check_file_exists(self, _file):
        return os.path.exists(f"{self._path}/{_file}")
    
    @staticmethod
    def _dep_maker(step, checkout, dep, exists: bool, graph: dict):
        if not checkout:
            checkout = '?'
        
        deps = []
        if checkout in graph:
            deps = graph[checkout]
        else:
            graph[checkout] = deps
        
        link = (step, 'file', dep if exists else f"Missing file {dep}")
        if link not in deps:
            deps += [link]

    def __check_file_usage(self, name, run, checkout, graph: dict):
        for cmd, _file in self.__cmds.items():
            if cmd in run:
                self._dep_maker(name, checkout, _file, self.__check_file_exists(_file), graph)
        
        run = run.replace("\n", " ")
        for arg in run.split(' '):
            if os.path.isfile(f"{self._path}/{arg}"):
                self._dep_maker(name, checkout, arg, self.__check_file_exists(arg), graph)
