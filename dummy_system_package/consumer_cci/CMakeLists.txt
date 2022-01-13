cmake_minimum_required(VERSION 3.1)
project(DigestConsumerCciTest)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(digest main.cpp)

find_package(Digest REQUIRED)

target_link_libraries(digest Digest::Digest)
