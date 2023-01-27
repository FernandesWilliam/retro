from src.dependency_parser.utils import job_names


def detect(yml):
    return { job: [] for job in job_names(yml) }

def links_dependencies(yml, job_map):
    def __needs (yaml, job):
        return yaml['jobs'][job]['needs'] if 'needs' in yaml['jobs'][job] else []
    
    return {
        job: [(need, 'seq', '') for need in __needs(yml, job)] 
        for job in job_map.keys()
    }

def build_graph(dot, dep):
    for node in dep.keys():
        dot.node(node)
    
    for job, dependencies in dep.items():
        for dep, _type, _ in dependencies:
            if _type == 'seq':
                dot.edge(dep, job)
