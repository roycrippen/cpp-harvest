from typing import Callable


class Config:
    def __init__(self):
        self.generator: Generator = Generator()
        self.app: App = App()


class Generator:
    def __init__(self):
        self.compiler = 'clang++'
        self.cflags = ''
        self.flags = None
        self.working_directory = '.'


class App:
    def __init__(self):
        self.exclude_files_start_with = []
        self.exclude_namespaces = []
        self.files = []
        self.reports = []


class Report:
    def __init__(self):
        self.func = staticmethod(print)
        self.run = False
        self.show_screen = True
        self.output_yaml = None
