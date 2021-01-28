//
// Created by roy.crippen on 1/26/21.
//
#include <iostream>

#include "foo.hpp"

int main() {
    auto s = "foo";
    std::cout << some_name_space::Foo::my_function(41, "Foo") << "\n";
    std::cout << some_name_space::FooAlias::my_function(41, "FooAlias") << "\n";
    std::cout << "add_one " << some_name_space::add_one(41) << "\n";
}