from pygccxml import utils
from pygccxml import declarations
from pygccxml import parser

if __name__ == '__main__':
    # Find the location of the xml generator (castxml or gccxml)
    generator_path, generator_name = utils.find_xml_generator()

    # Configure the xml generator
    xml_generator_config = parser.xml_generator_configuration_t(
        xml_generator_path=generator_path,
        xml_generator=generator_name)

    # The c++ file we want to parse
    filename = "declaration_compare.hpp"

    # Parse the c++ file
    decls = parser.parse([filename], xml_generator_config)

    global_namespace = declarations.get_global_namespace(decls)

    ns_namespace = global_namespace.namespace("ns")

    # Search for the function called func1
    criteria = declarations.calldef_matcher(name="func1")
    func1a = declarations.matcher.get_single(criteria, ns_namespace)

    # Search for the function called func2
    criteria = declarations.calldef_matcher(name="func2")
    func2a = declarations.matcher.get_single(criteria, ns_namespace)

    # You can also write a loop on the declaration tree
    func1b = None
    for decl in ns_namespace.declarations:
        if decl.name == "func1":
            func1b = decl

    # The declarations can be compared (prints (True, False))
    print(func1a == func1b, func1a == func2a)