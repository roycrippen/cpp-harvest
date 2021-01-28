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
    filename = "functions_and_arguments.hpp"

    decls = parser.parse([filename], xml_generator_config)
    global_namespace = declarations.get_global_namespace(decls)
    ns = global_namespace.namespace("ns")

    # Use the free_functions method to find our function
    func = ns.free_function(name="myFunction")

    # There are two arguments:
    print(len(func.arguments))

    # We can loop over them and print some information:
    for arg in func.arguments:
        print(
            arg.name,
            str(arg.decl_type),
            declarations.is_std_string(arg.decl_type),
            declarations.is_reference(arg.decl_type))
