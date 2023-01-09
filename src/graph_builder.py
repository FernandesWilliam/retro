from graphviz import Digraph
from abc import ABC, abstractmethod


ERROR_EDGE = '?'


class GraphBuilder(ABC):
    def __init__(self, data):
        self._data = data

    @abstractmethod
    def generate(self, filename, **kwargs):
        pass


class DotGraphBuilder(GraphBuilder):
    """
    Doc for styling: https://graphviz.org/doc/info/attrs.html
    Check this for example: https://www.graphviz.org/gallery/
    """
    __style = {
        'seq': {'style': 'dotted'},
        'up/down': {'decorate': 'false'},
        'release': {'style': 'dashed'}
    }

    def __init__(self, data: dict[str, list[tuple]]):
        """
        :param data: Expected format: `{'node1': [('dest_node', 'link_type', 'msg')], 'node2': []}`
        """
        super().__init__(data)

    def generate(self, filename, file_format="png", output_dir='images', **kwargs):
        graph = Digraph(filename=filename, format=file_format, **kwargs)

        for node in self._data.keys():
            graph.node(node)

        graph.node(ERROR_EDGE, shape='ellipse')

        for node, edges in self._data.items():
            for dest, edge_type, msg in edges:
                if edge_type not in self.__style.keys():
                    raise KeyError("Edge type unknown %s" % edge_type)

                style = {}
                if dest == ERROR_EDGE:
                    style['color'] = 'orange'

                graph.edge(node, dest, xlabel=msg, **self.__style[edge_type], **style)

        return graph.render(directory=output_dir)
