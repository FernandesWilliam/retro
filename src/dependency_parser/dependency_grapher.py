from src.parser import yaml_parse
from importlib import import_module
import graphviz
import logging


def generate_graph(file_name, graph):
    """Generate a graphviz image representation of a graph"""
    logger = logging.getLogger(__name__)
    final_filename = file_name.split('/')[-1].replace('.yml', '.dot')
    dot = graphviz.Digraph(filename=final_filename, format="png")
    logger.info(f"Creating {final_filename} images from the graph which come from {file_name}")
    # for each studied patterns, build a graph.
    for key in graph.keys():
        for pattern in graph[key]:
            graph[key][pattern]['graph_loader'](dot,graph[key][pattern]['dep'])

    #render graph
    logger.info('Resulting file: %s' % dot.render(directory='images'))


# This function first detects patterns of a file, then processed them and make a graph that belongs to inter and intra dependencies relation
def make_graph(file_name, watching_dependencies={}):
    yml = yaml_parse(file_name)
    graph = {}
    # dynamic import of a file, it could belong to inter package or intra
    def import_pattern(type_dep, module):
        return import_module(f"src.dependency_parser.{type_dep}_patterns.{module}")

    # load all required modules and assign to graph type : intra || inter -> a dict with 2 keys module and dependencies
    for key, modules in watching_dependencies.items():
        modules = {module: import_pattern(key, module) for module in modules}
        # identifies all dependency that match with the current one evaluated
        detected_pattern = {module: modules[module].detect(yml) for module in modules.keys()}

        graph[key] = {module: {'dep': modules[module].links_dependencies(yml, detected_pattern[module]),
                               'graph_loader': modules[module].build_graph} for module in modules.keys()}

    generate_graph(file_name,graph)
