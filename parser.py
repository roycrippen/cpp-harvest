from copy import copy
from typing import List

import pygccxml
from pygccxml import declarations
from pygccxml import utils

from config import App


def parse(config):
    generator_path, generator_name = utils.find_xml_generator()
    xml_config = pygccxml.parser.xml_generator_configuration_t(
        xml_generator_path=generator_path,
        xml_generator=generator_name,
        compiler=config.generator.compiler,
        cflags=config.generator.cflags,
        flags=config.generator.flags,
        working_directory=config.generator.working_directory)

    decls = pygccxml.parser.parse(config.app.files, xml_config)
    tree = Tree(config.app, decls)
    return tree


class DeclaredType:
    def __init__(self, d):
        self.decl_string = d.decl_string
        self.display = d.decl_string
        self.byte_size = int(d.byte_size)
        self.loc_file_name = None
        self.loc_line = None
        if hasattr(d, 'declaration') and hasattr(d.declaration, 'location'):
            self.loc_file_name = d.declaration.location.file_name
            self.loc_line = d.declaration.location.line


class TypeDef:
    def __init__(self, d: declarations.typedef_t):
        self.name = d.name
        self.decl_string = d.decl_string
        self.decl_type = DeclaredType(d.decl_type)
        self.display = f'[typedef] {self.name}, type: {self.decl_type.display}'


class MemberOperator:
    def __init__(self, d: declarations.member_operator_t):
        self.name = d.name
        self.decl_string = d.decl_string
        self.symbol = d.symbol
        self.display = f'[member operator] {self.decl_string}, symbol: {self.symbol}'


class Enumeration:
    def __init__(self, d: declarations.enumeration_t):
        self.name = d.name
        self.decl_string = d.decl_string
        self.values = str(d.values)
        self.display = f'[enumeration] {self.decl_string}'


class Argument:
    def __init__(self, d: declarations.argument_t):
        self.name = d.name
        self.decl_string = str(d)
        self.decl_type = DeclaredType(d.decl_type)
        self.display = f'[argument] {self.name}, type: {self.decl_type.display}'


class Variable:
    def __init__(self, d: declarations.variable_t):
        self.key = d.decl_string
        self.name = d.name
        self.decl_type = DeclaredType(d.decl_type)
        self.loc_file_name = d.location.file_name
        self.loc_line = d.location.line
        self.display = f'[variable] {self.key}, type: {self.decl_type.display}'


class FreeFunction:
    def __init__(self, d: declarations.free_function_t):
        self.declaration = str(d)[:-15]
        self.name = d.name
        self.key = self.declaration
        self.return_type = DeclaredType(d.return_type)
        self.does_throw = d.does_throw
        self.display = f'[free function] {self.key}'


class MemberFunction:
    def __init__(self, d: declarations.member_function_t):
        self.declaration = str(d)[:-18]
        self.name = d.name
        self.key = self.declaration
        self.return_type = DeclaredType(d.return_type)
        self.does_throw = d.does_throw
        self.virtuality = d.virtuality
        self.has_static = bool(int(d.has_static))
        self.display = f'[member function] {self.key}'


class Private:
    def __init__(self):
        self.display = 'Private'


class Protected:
    def __init__(self):
        self.display = 'Protected'


class Public:
    def __init__(self):
        self.display = 'Public'


class ClassDeclaration:
    def __init__(self, d: declarations.class_declaration_t):
        self.name = d.name
        self.key = d.decl_string
        self.display = f'[class declaration] {self.key}'


class Constructor:
    def __init__(self, d: declarations.constructor_t):
        self.name = d.name
        self.key = d.decl_string
        self.display = f'[constructor] {self.key}'


class Destructor:
    def __init__(self, d: declarations.destructor_t):
        self.name = d.name
        self.key = d.decl_string
        self.display = f'[destructor] {self.key}'


class Unknown:
    def __init__(self, d):
        self.display = str(d)
        self.name = d.name
        self.key = d.decl_string


class Klass:
    def __init__(self, d: declarations.class_t):
        self.name = d.name
        self.key = d.decl_string
        self.private = Private()
        self.protected = Protected()
        self.public = Public()
        self.display = f'[{d.class_type}] {self.key}'


class NameSpace:
    def __init__(self, d: declarations.namespace_t):
        self.name = d.name
        self.key = d.decl_string
        self.display = f'[namespace] {self.name}'


class Tree:
    def __init__(self, cfg: App, decls):
        self.nss = []
        self.namespaces = dict()
        self.classes = dict()
        self.member_functions = dict()
        self.variables = dict()
        self.free_functions = dict()
        self.__build_tree(cfg, decls)

    def __build_tree(self, cfg: App, decls):
        def go(tree, ds: List):
            for d in ds:
                # ignore excluded files
                if is_excluded(d, cfg.exclude_files_start_with):
                    continue

                # recursively build tree by type of 'd'
                # namespace
                if isinstance(d, declarations.namespace_t):
                    if d.decl_string in cfg.exclude_namespaces:
                        continue
                    else:
                        ns = go(NameSpace(d), d.declarations)
                        append(tree, ns, 'nss')
                        self.namespaces[ns.key] = ns
                # class
                elif isinstance(d, declarations.class_t):
                    kl = Klass(d)
                    kl.private = go(kl.private, d.private_members)
                    kl.protected = go(kl.protected, d.protected_members)
                    kl.public = go(kl.public, d.public_members)
                    append(tree, kl, 'classes')
                    self.classes[kl.key] = kl
                # member function
                elif isinstance(d, declarations.member_function_t):
                    f = go(MemberFunction(d), d.arguments)
                    append(tree, f, 'member_functions')
                    self.member_functions[f.key] = f
                # free function
                elif isinstance(d, declarations.free_function_t):
                    f = go(FreeFunction(d), d.arguments)
                    append(tree, f, 'free_functions')
                    self.free_functions[f.key] = f
                # variable
                elif isinstance(d, declarations.variable_t):
                    v = Variable(d)
                    append(tree, v, 'variables')
                    self.variables[v.key] = v
                # argument
                elif isinstance(d, declarations.argument_t):
                    arg = Argument(d)
                    append(tree, arg, 'arguments')
                # typedef
                elif isinstance(d, declarations.typedef_t):
                    append(tree, TypeDef(d), 'typedefs')
                # constructor
                elif isinstance(d, declarations.constructor_t):
                    append(tree, Constructor(d), 'constructors')
                # destructor
                elif isinstance(d, declarations.destructor_t):
                    append(tree, Destructor(d), 'destructors')
                # member_operator
                elif isinstance(d, declarations.member_operator_t):
                    append(tree, MemberOperator(d), 'member_operator')
                # declarations.enumeration
                elif isinstance(d, declarations.enumeration_t):
                    append(tree, Enumeration(d), 'enumerations')
                # class_declaration
                elif isinstance(d, declarations.class_declaration_t):
                    append(tree, ClassDeclaration(d), 'class_declarations')
                    pass
                # unknown
                else:
                    append(tree, Unknown(d), 'unknowns')
                    pass

                # end for
            # end go
            return tree

        t = go(self, decls)
        return t

    @staticmethod
    def __separate(obj):
        ls = []
        new_obj = copy(obj)
        for k, v in vars(obj).items():
            if isinstance(v, list) and not isinstance(v, tuple):
                ls.append(v)
                delattr(new_obj, k)
            elif k in ['private', 'protected', 'public']:
                ls.append([v])
                delattr(new_obj, k)
        return ls, new_obj

    def walk(self):
        def go(xs, indent, ds):
            for d in ds:
                lss, obj = self.__separate(d)
                obj.indent = indent
                if hasattr(obj, 'private'):
                    pass
                xs.append(obj)
                for ls in lss:
                    go(xs, indent + '  ', ls)
            return xs

        res = go([], '', self.nss)
        return res


def is_excluded(d, excludes):
    if d is None:
        return False
    if hasattr(d, 'location') and isinstance(d.location, declarations.location_t):
        return any(d.location.file_name.startswith(exclude) for exclude in excludes)
    else:
        return False


def append(tree, value, attribute_name):
    if hasattr(tree, attribute_name):
        xs = getattr(tree, attribute_name)
        xs.append(value)
    else:
        setattr(tree, attribute_name, [value])
