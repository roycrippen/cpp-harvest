import os
import sys

import yaml

from config import Config
from parser import parse, Tree
from reports import Reports


def main(argv):
    # read config
    config_file = 'examples/tiny_config.yaml'
    if len(argv) > 0:
        config_file = argv[0]

    config: Config = read_yaml(config_file)
    if config is None:
        print(f'Failed to read config file: {config_file}')
        print('aborting')
        sys.exit(-1)

    # build the tree
    tree: Tree = parse(config)
    result_yaml = yaml.dump(tree, default_flow_style=False, width=240)

    # run reports
    reports = Reports(tree, config)
    reports.run()


def read_yaml(f_name: str):
    res = None
    try:
        with open(f_name) as f:
            res = yaml.load(f, Loader=yaml.FullLoader)
    except IOError as error:
        print(error)

    return res


if __name__ == '__main__':
    main(sys.argv[1:])
