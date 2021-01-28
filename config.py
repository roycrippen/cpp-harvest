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
        self.result_yaml = 'results.yaml'
        self.print_result = True
        self.test_walk = True
