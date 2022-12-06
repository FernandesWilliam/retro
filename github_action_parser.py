import yaml
import graphviz
import logging


def parse(file_name, parsers):
    with open(file_name, "r") as stream:
        try:
            yml = yaml.safe_load(stream)
            for depName, parser in parsers:
                generateGraph(file_name, parser(yml))
        except yaml.YAMLError as exc:
            print(exc)


def downloadAction(map, yml, job, step):
    if step['with']['name'] not in map.keys():
        map[step['with']['name']] = {}
        map[step['with']['name']]['producer'] = "?"
        map[step['with']['name']]['consumer'] = []
        map[step['with']['name']]['consumer'] += [job]
        map[step['with']['name']]['producer_prevention'] = [
            {'warning': 'red', 'error': "Unknown Artifacts : " + job, 'cause': job}]

    elif map[step['with']['name']]['producer'] in yml['jobs'][job]['needs']:
        map[step['with']['name']]['consumer'] += [job]
    else:
        # Require to add a need
        map[step['with']['name']]['consumer_prevention'] = [
            {'warning': 'red', 'error': "missing needs :" + job, 'cause': job}]


def uploadAction(map, yml, job, step):
    map[step['with']['name']] = {'producer': job, 'consumer': []}


def getSteps(yml, job):
    return yml['jobs'][job]['steps']


# up_down
toWatch = {
    'actions/upload': uploadAction,
    'actions/download': downloadAction,
    'actions/release': lambda: ...,
}


# "[ dep 1 |de p  |]"
def generateGraph(filename, dep):
    """Generate a graphviz image representation of a graph"""
    logger = logging.getLogger(__name__)

    final_filename = filename.split('/')[-1].replace('.yml', '.dot')
    dot = graphviz.Digraph(filename=final_filename, format="png")
    logger.info("Dependencies: %s" % dep)
    for key in dep.keys():
        dot.node(dep[key]['producer'])
        if 'consumer_prevention' in dep[key]:
            for prev in dep[key]['consumer_prevention']:
                dot.node(prev['cause'])

                dot.edge(dep[key]['producer'], prev['cause'], label=prev['error'] + key, color=prev['warning'])

        if 'producer_prevention' in dep[key]:
            for prev in dep[key]['producer_prevention']:
                dot.node(prev['cause'])

                dot.edge(dep[key]['producer'], prev['cause'], label=prev['error'] + key, color=prev['warning'])

        else:
            for consumer in dep[key]['consumer']:
                dot.node(consumer)
                dot.edge(dep[key]['producer'], consumer, label=key)

    logger.info('Resulting file: %s' % dot.render(directory='images'))


def inter_dependency_parsing(yml):
    mapDependency = {}
    # {i:x for i,x in enumerate(a)}

    isAWatchingDep = lambda step: list(filter(lambda key: key in step['uses'], toWatch.keys()))

    extractUses = lambda yml, job: [step for step in getSteps(yml, job) if 'uses' in step and isAWatchingDep(step)]

    matchings = {job: extractUses(yml, job) for job in yml['jobs'].keys()}
    # print(matchings)
    for matching in matchings.keys():
        for valid in matchings[matching]:
            for watch in toWatch.keys():
                if watch not in valid['uses']:
                    continue

                toWatch[watch](mapDependency, yml, matching, valid)

    return mapDependency
