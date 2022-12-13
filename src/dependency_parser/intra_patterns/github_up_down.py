from src.dependency_parser.utils import steps, job_names


def download_link(linked_dep, yml, job, action):
    download_dep = action['with']['name']

    # if the download dep still doesn't exist it is caused due to unknown artefact
    if download_dep not in linked_dep.keys():
        linked_dep[download_dep] = {
            'producer': 'Unknown',
            'consumer': [job],
            'producer_inconsistency': [
                {'warning': 'orange', 'problem': f"Artifacts {download_dep} not declared : "}
            ]
        }
    elif 'needs' in yml['jobs'][job] and linked_dep[download_dep]['producer'] in yml['jobs'][job]['needs']:
        linked_dep[download_dep]['consumer'] += [job]
    # In case needs are missing.
    else:
        linked_dep[download_dep]['consumer'] += [job]
        linked_dep[download_dep]['consumer_inconsistency'] = [
            {'warning': 'orange', 'problem': "Missing Needs for job : " + linked_dep[download_dep]['producer']}
        ]


# Find out every upload pattern, and store the upload as producer job
def upload_link(linked_dep, yml, job, action):
    linked_dep[action['with']['name']] = {'producer': job, 'consumer': []}


pattern = {
    'actions/upload': upload_link,
    'actions/download': download_link,
}


# find if there is any pattern that match with the current configuration.
def detect(yml):
    # verify that a step match with an upload or download pattern
    def match_with_pattern(step):
        return list(filter(lambda key: key in step['uses'], pattern.keys()))

    # an array of tuples that contains all steps that match with a pattern, (is_dep,relation object)
    def matching_steps(yml, job):
        _steps = {patternKey: [] for patternKey in pattern.keys()}
        is_dep = False
        for step in steps(yml, job):
            if 'uses' not in step or len((match := match_with_pattern(step))) == 0: continue
            _steps[match[0]] += [step]
            is_dep = True

        return (is_dep, _steps)

    # a map which contains as key job names and as values : steps that contains a pattern actions.
    job_map = {job: match[1] for job in job_names(yml) if ((match := matching_steps(yml, job))[0])}

    return job_map

# Run every pattern and add a new linked dependency into the linked_dep.
def links_dependencies(yml, job_map):
    linked_dep = {}
    for job, matching_steps in job_map.items():
        for pattern_name, actions in matching_steps.items():
            for action in actions:
                pattern[pattern_name](linked_dep, yml, job, action)
    return linked_dep


def build_graph(dot, dep):
    for artefact in dep.keys():
        # append the artefact creator
        producer = dep[artefact]['producer']
        dot.node(producer)

        if 'consumer_inconsistency' in dep[artefact]:
            for inconsistency in dep[artefact]['consumer_inconsistency']:
                for consumer in dep[artefact]['consumer']:
                    dot.edge(producer, consumer, label=inconsistency['problem'], color=inconsistency['warning'])

        elif 'producer_inconsistency' in dep[artefact]:
            for inconsistency in dep[artefact]['producer_inconsistency']:
                for consumer in dep[artefact]['consumer']:
                    dot.edge(dep[artefact]['producer'], consumer, label=inconsistency['problem'],
                         color=inconsistency['warning'])
        # Normal case
        else:
            for consumer in dep[artefact]['consumer']:
                dot.node(consumer)
                dot.edge(dep[artefact]['producer'], consumer, label=artefact)
