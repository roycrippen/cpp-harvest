#include <cstdint>
#include <string>
#include <utility>
#include "unittests.hpp"

#ifndef FOO_HPP
#define FOO_HPP

namespace some_name_space {

    struct Foo {
    public:
        Foo() = default;

        Foo(uintmax_t a, uintmax_t b, unittests::test_suite tests, char c, float d) : a(a), b(b),
                                                                                      tests(std::move(tests)),
                                                                                      c(c), d(d) {}

        uintmax_t a = 0, b = 0;

        unittests::test_suite tests = unittests::test_suite();

        static std::string my_function(int v, const std::string &x1) {
            return x1 + " " + std::to_string(v + 1);
        }

    private:
        char c = 'a';
    protected:
        float d = 0.0f;
    };

    typedef Foo FooAlias;

    int add_one(int a) {
        return a + 1;
    }

}

#endif