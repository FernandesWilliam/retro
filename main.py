# from github_action_parser import parse, inter_dependency_parsing
from argparse import ArgumentParser
from downloader import Downloader

# parse("./repositories/audacity/build.yml", [
#     ("up_down", inter_dependency_parsing)
#
#     ])
#
#
# parse("./repositories/juicyshop/ci.yml", [
#     ("up_down", inter_dependency_parsing)
#
#     ])


def main():
    parser = ArgumentParser(prog="GitHub Action Analyser")

    parser.add_argument("git_url")

    args = parser.parse_args()

    # print(args.repository)
    Downloader(args.git_url).download()

    while True:
        pass


if __name__ == "__main__":
    main()
