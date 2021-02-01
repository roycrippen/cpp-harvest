import os

import yaml

from config import Report, Config
from parser import Tree


class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True


class Reports:
    def __init__(self, tree: Tree, config: Config):
        self.tree = tree
        self.config = config

    def run(self):
        for report_dict in self.config.app.reports:
            report: Report = list(report_dict.values())[0]
            eval(f'self.{report.func}')(report)
            pass

    def write_yaml(self, yaml_str: str, file_name: str):
        result_file = os.path.join(self.config.generator.working_directory, file_name)
        print(f'writing yaml file: {result_file}')
        with open(result_file, 'w') as f:
            f.write(yaml_str)

    def run_test_walk(self, report: Report):
        if not report.show_screen and report.output_yaml is None:
            return

        objs = self.tree.walk()

        if report.show_screen:
            print('\ntesting tree.walk()...')
            for obj in objs:
                if hasattr(obj, 'display') and hasattr(obj, 'indent'):
                    print(f'{obj.indent}{obj.display}')
                else:
                    print(f'type = {type(obj).__name__}')

        if report.output_yaml is not None:
            self.write_yaml(yaml.dump(objs, Dumper=NoAliasDumper, default_flow_style=False, indent=4, width=240),
                            report.output_yaml)

    def run_result_report(self, report: Report):
        if not report.show_screen and report.output_yaml is None:
            return

        yaml_str = yaml.dump(self.tree, Dumper=NoAliasDumper, default_flow_style=False, indent=4, width=240)

        # approximately 4 times smaller with references
        # yaml_str = yaml.dump(self.tree, default_flow_style=False, indent=4, width=240)

        if report.show_screen:
            print('\nprint tree in yaml format...')
            print(yaml_str)

        if report.output_yaml is not None:
            self.write_yaml(yaml_str, report.output_yaml)
