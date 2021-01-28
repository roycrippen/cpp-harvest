from pygccxml import utils
from pygccxml import declarations
from pygccxml import parser

if __name__ == '__main__':
    # Find out the c++ parser
    generator_path, generator_name = utils.find_xml_generator()

    # Configure the xml generator
    xml_generator_config = parser.xml_generator_configuration_t(
        xml_generator_path=generator_path,
        xml_generator=generator_name)

    # The c++ file we want to parse
    filename = "nested_types.hpp"

    decls = parser.parse([filename], xml_generator_config)
    global_namespace = declarations.get_global_namespace(decls)
    ns = global_namespace.namespace("ns")

    a = ns.variables()[0]

    print("My name is: " + a.name)
    # > My name is: a

    print("My type is: " + str(a.decl_type))
    # > My type is: int const

    # If we print real python type:
    print("My type is : " + str(type(a.decl_type)))
    # > My type is: <class 'pygccxml.declarations.cpptypes.const_t'>

    # Types are nested in pygccxml. This means that you will get information
    # about the first type only. You can access the "base" type by removing
    # the const part:
    print("My base type is: " + str(type(declarations.remove_const(a.decl_type))))
    # > My base type is: <class 'pygccxml.declarations.cpptypes.int_t'>

    # You use the is_const function to check for a type:
    print("Is 'a' a const ?: " + str(declarations.is_const(a.decl_type)))
    # > Is 'a' a const ?: True

    # A more complex example with variable b:
    b = ns.variables()[1]
    print("My type is: " + str(type(b.decl_type)))
    # > My type is: <class 'pygccxml.declarations.cpptypes.pointer_t'>
    print("My type is: " + str(type(
        declarations.remove_const(
            declarations.remove_volatile(
                declarations.remove_pointer(b.decl_type))))))
    # > My type is: <class 'pygccxml.declarations.cpptypes.int_t'>

    # The declarations module contains much more methods allowing you to
    # navigate the nested types list.