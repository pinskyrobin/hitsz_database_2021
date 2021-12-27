cmake_minimum_required(VERSION 3.20)
project(Exp5 C)
set(CMAKE_C_STANDARD 99)
include_directories("./")
add_library(extmem  extmem.c)

add_executable(exec solution.c utils.h)

target_link_libraries(exec extmem)