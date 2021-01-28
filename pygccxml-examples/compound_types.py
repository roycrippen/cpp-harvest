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
    filename = "compound_types.hpp"

    decls = parser.parse([filename], xml_generator_config)
    global_namespace = declarations.get_global_namespace(decls)

    c1 = global_namespace.variable("c1")
    print(str(c1), type(c1))
    # > 'c1 [variable]', <class 'pygccxml.declarations.variable.variable_t'>

    print(str(c1.decl_type), type(c1.decl_type))
    # > 'int const', <class 'pygccxml.declarations.cpptypes.const_t'>

    base = declarations.remove_const(c1.decl_type)
    print(str(base), type(base))
    # > 'int', <class 'pygccxml.declarations.cpptypes.int_t'>

    c2 = global_namespace.variable("c2")
    print(str(c2.decl_type), type(c2.decl_type))
    # > 'int const', <class 'pygccxml.declarations.cpptypes.const_t'>
    # Even if the declaration was defined as 'const int', pygccxml will always
    # output the const qualifier (and some other qualifiers) on the right hand
    # side (by convention).

    cv1 = global_namespace.variable("cv1")
    print(str(cv1.decl_type), type(cv1.decl_type))
    # > 'int const volatile', <class 'pygccxml.declarations.cpptypes.volatile_t'>

    # Remove one level:
    base = declarations.remove_volatile(cv1.decl_type)
    print(str(base), type(base))
    # > 'int const', <class 'pygccxml.declarations.cpptypes.const_t'>

    # Remove the second level:
    base = declarations.remove_const(base)
    print(str(base), type(base))
    # > 'int', <class 'pygccxml.declarations.cpptypes.int_t'>

    # We can also directly do this in one step:
    base = declarations.remove_cv(cv1.decl_type)
    print(str(base), type(base))
    # > 'int', <class 'pygccxml.declarations.cpptypes.int_t'>

    # As for consts, the const and volatile are on the right hand side
    # (by convention), and always in the same order
    cv2 = global_namespace.variable("cv2")
    print(str(cv2.decl_type), type(cv2.decl_type))
    # > 'int const volatile', <class 'pygccxml.declarations.cpptypes.volatile_t'>

    # And a last example with a pointer_t:
    cptr1 = global_namespace.variable("cptr1")
    print(str(cptr1.decl_type), type(cptr1.decl_type))
    # > 'int const * const', <class 'pygccxml.declarations.cpptypes.const_t'>)

    base = declarations.remove_const(cptr1.decl_type)
    print(str(base), type(base))
    # > 'int const *', <class 'pygccxml.declarations.cpptypes.pointer_t'>

    base = declarations.remove_pointer(base)
    print(str(base), type(base))
    # > 'int const', <class 'pygccxml.declarations.cpptypes.const_t'>)

    base = declarations.remove_const(base)
    print(str(base), type(base))
    # > 'int', <class 'pygccxml.declarations.cpptypes.int_t'>)
