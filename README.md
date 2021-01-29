# python application to help analyze cpp source code
requires
- [python 3.x](https://www.python.org/download/releases/3.0/) 
- [pygccxml](https://github.com/CastXML/pygccxml)  
- [g++](https://gcc.gnu.org/) or [clang++](https://clang.llvm.org/cxx_status.html) <br><br>

pygccxml can be installed with `sudo apt install pygccxml` on Ubuntu

## quick start
```
$ python3 main.py examples/tiny/tiny_config.yaml
```
or
```
$ python main.py examples/foo/foo_config.yaml
```

## config file examples
[foo_config.yaml](./examples/foo/foo_config.yaml) <br>
[tiny_config.yaml](./examples/tiny/tiny_config.yaml) <br>

## run pygccxml examples
The pygccxml folder contains the pygccxml tutorial examples. <br>
Each `some_example.py` file  has a `some_example.hpp` data file that is compiled and parsed. <br>
For example to run the `declaration.py` example:
```bash
$ cd pygccxml-examples
$ python3 declaration.py 
```
