from pygccxml import declarations
from pygccxml import parser
from pygccxml import utils

if __name__ == '__main__':
    # Find out the c++ parser
    generator_path, generator_name = utils.find_xml_generator()

    # Configure the xml generator
    xml_generator_config = parser.xml_generator_configuration_t(
        xml_generator_path=generator_path,
        xml_generator=generator_name)

    # The c++ file we want to parse
    filename = "function_pointer.hpp"

    decls = parser.parse([filename], xml_generator_config)
    global_namespace = declarations.get_global_namespace(decls)

    function_ptr = global_namespace.variables()[0]

    # Print the name of the function pointer
    print(function_ptr.name)
    # > myFuncPointer

    # Print the type of the declaration
    print(function_ptr.decl_type)
    # > void (*)( int,double )

    # Print the real type of the declaration (it's just a pointer)
    print(type(function_ptr.decl_type))
    # > <class 'pygccxml.declarations.cpptypes.pointer_t'>

    # Check if this is a function pointer
    print(declarations.is_calldef_pointer(function_ptr.decl_type))
    # > True

    # Remove the pointer part, to access the function's type
    f_type = declarations.remove_pointer(function_ptr.decl_type)

    # Print the type
    print(type(f_type))
    # > <class 'pygccxml.declarations.cpptypes.free_function_type_t'>

    # Print the return type and the arguments of the function
    print(f_type.return_type)
    # > void

    # Print the return type and the arguments
    print(str(f_type.arguments_types[0]), str(f_type.arguments_types[1]))
    # > int, double
