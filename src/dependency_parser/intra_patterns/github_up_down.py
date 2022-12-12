from src.dependency_parser.utils import steps, job_names


def download_link(linked_dep, yml, job, action):
    download_dep = action['with']['name']
    # if the download dep still doesn't exist it is caused due to unknown artefact
    if download_dep not in linked_dep.keys():
        linked_dep[download_dep] = {
            'producer': 'Unknown',
            'consumer': linked_dep[download_dep]['consumer'] + [job],
            'producer_inconsistency': [
                {'warning': 'orange', 'problem': "Artifacts Not Declared : " + job}
            ]
        }
    elif 'needs' in yml['jobs'][job] and linked_dep[download_dep]['producer'] in yml['jobs'][job]['needs']:
        linked_dep[download_dep]['consumer'] += [job]

    else:
        linked_dep[download_dep]['consumer_inconsistency'] = [
            {'warning': 'orange', 'problem': "Missing Needs " + job}
        ]


def upload_link(linked_dep, yml, job, action):
    linked_dep[action['with']['name']] = {'producer': job, 'consumer': []}


pattern = {
    'actions/upload': upload_link,
    'actions/download': download_link,
}


def detect(yml):
    # verify that a step match with a upload or download pattern
    def match_with_pattern(step):
        return list(filter(lambda key: key in step['uses'], pattern.keys()))

    # an array that contains all steps that match with a pattern
    def matching_steps(yml, job):
        _steps = dict.fromkeys(pattern.keys(), [])
        is_dep = False

        for step in steps(yml, job):
            if 'uses' not in step or len((match := match_with_pattern(step))) == 0: continue
            _steps[match[0]] += [step]
            is_dep = True

        return (is_dep, _steps)

    # a map which contains as key job names and as values : steps that contains a pattern actions.
    job_map = {job: match[1] for job in job_names(yml) if ((match := matching_steps(yml, job))[0])}

    return job_map


def links_dependencies(yml, job_map):
    linked_dep = {}
    for job, matching_steps in job_map.items():
        for pattern_name, actions in matching_steps.items():
            for action in actions:
                pattern[pattern_name](linked_dep, yml, job, action)
    return linked_dep

def build_graph(dot,dep):
    print(dep)
    for artefact in dep.keys():
        # append the artefact creator
        producer=dep[artefact]['producer']
        dot.node(producer)
        if 'consumer_inconsistency' in dep[artefact]:
            print(dep[artefact]['consumer_inconsistency'])
            for inconsistency in dep[artefact]['consumer_inconsistency']:

                dot.edge(producer, inconsistency['problem'], label=inconsistency['problem'], color= inconsistency['warning'])

        if 'producer_prevention' in dep[artefact]:
            for prev in dep[artefact]['producer_prevention']:
                dot.node(prev['cause'])

                dot.edge(dep[artefact]['producer'], prev['cause'], label=prev['error'] + artefact, color=prev['warning'])

        else:
            for consumer in dep[artefact]['consumer']:
                dot.node(consumer)
                dot.edge(dep[artefact]['producer'], consumer, label=artefact)


