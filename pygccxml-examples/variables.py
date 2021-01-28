import pprint

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
    filename = "variables.hpp"
    decls = parser.parse([filename], xml_generator_config)
    global_namespace = declarations.get_global_namespace(decls)
    ns = global_namespace.namespace("ns")

    variables = []
    for var in ns.variables():
        variable = {'name': var.name, 'type': str(var.decl_type), 'value': var.value}
        variables.append(variable)

    ns = {'namespace': 'ns', 'variables': variables}
    pp = pprint.PrettyPrinter(indent=4, width=120)
    pp.pprint(ns)


