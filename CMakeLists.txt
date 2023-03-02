cmake_minimum_required(VERSION 3.8)
project(fast_hit_emu)

set(CMAKE_CXX_STANDARD 11)

find_package(pybind11 REQUIRED)

file(GLOB_RECURSE SOURCES src/**.cpp)
add_library(fast_hit_emu_lib SHARED ${SOURCES})
target_include_directories(fast_hit_emu_lib PUBLIC ./include)

pybind11_add_module(fast_hit_emu pybindsrc/fast_hit_emu.cpp)
target_link_libraries(fast_hit_emu PRIVATE fast_hit_emu_lib)

#add_subdirectory(pybindsrc)