import os
import sys

import yaml

from config import Config
from parser import parse, Tree


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

    # print results?
    if config.app.print_result:
        print('\nprinting YAML result...')
        print(result_yaml)

    # write results to YAML file
    result_file = os.path.join(config.generator.working_directory, config.app.result_yaml)
    with open(result_file, 'w') as f:
        f.write(result_yaml)

    # test YAML file
    _yaml = read_yaml(result_file)
    assert _yaml is not None

    # test walk?
    if config.app.test_walk:
        print('\ntesting tree.walk()...')
        objs = tree.walk()
        for obj in objs:
            if hasattr(obj, 'display'):
                print(f'{obj.indent}{obj.display}')
            else:
                print(f'type = {type(obj).__name__}')
    pass


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
