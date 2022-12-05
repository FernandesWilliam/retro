from github_action_parser import parse, inter_dependency_parsing

parse("./repositories/audacity/build.yml", [
    ("up_down", inter_dependency_parsing)

    ])


parse("./repositories/juicyshop/ci.yml", [
    ("up_down", inter_dependency_parsing)

    ])
