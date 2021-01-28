cmake_minimum_required(VERSION 3.12)
project(Foo)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_C_COMPILER "clang")
set(CMAKE_CXX_COMPILER "/usr/bin/clang++")

message("compiler ==> " ${CMAKE_CXX_COMPILER})


add_executable(foo main.cpp foo.hpp)