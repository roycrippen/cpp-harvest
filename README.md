# python application to help analyze cpp source code
requires
- [python 3.x](https://www.python.org/download/releases/3.0/) 
- [pygccxml](https://github.com/CastXML/pygccxml)  
- [g++](https://gcc.gnu.org/) or [clang++](https://clang.llvm.org/cxx_status.html) <br><br>

pygccxml can be installed with ```sudo apt install pygccxml``` on Ubuntu

## quick start
```
$ python3 main.py examples/tiny/tiny_config.yaml
```
or
```
$ python main.py examples/foo/foo_config.yaml
```

## config file example
```yaml
# configuration file for cpp-harvest application
# maps directly to Config, Generator and App classes
# changes to yaml keys should also be made to the python class in config.py

!!python/object:config.Config

# pygccxml.parser.config options
# https://pygccxml.readthedocs.io/en/develop/apidocs/pygccxml.parser.config.html
generator: !!python/object:config.Generator
  # compiler: clang++
  compiler: g++
  cflags: ""
  flags: null
  working_directory: ./examples/tiny

# runtime application parameters
app: !!python/object:config.App
  # reduce the result set by excluding system and/or other file sets
  exclude_files_start_with: []

   # reduce the result set by excluding specific namespaces
  exclude_namespaces: []

  # c++ files to harvest
  # "#include" files will be included automatically
  files: [tiny.hpp]

  result_yaml: tiny_results.yaml
  print_result: true
  test_walk: true
```