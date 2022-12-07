

def steps(yml,job):
    return yml['jobs'][job]['steps']

def job_names(yml):
    return  yml['jobs'].keys()