cmake_minimum_required(VERSION 4.0)
set (CMAKE_CXX_COMPILER /usr/bin/g++-15)
project(my-project LANGUAGES CXX VERSION 0.0.1)
set (CMAKE_CXX_STANDARD 23)
set (CMAKE_CXX_STANDARD_REQUIRED ON)
set (CMAKE_CXX_EXTENSIONS OFF)
set (CMAKE_EXPORT_COMPILE_COMMANDS ON)
Include(FetchContent)
# add all executables
add_executable(demo7 src/demo7.cpp )
add_executable(my_test_7_test tests/my_test_7.cpp )
add_library(my_headers0 INTERFACE)
target_include_directories(my_headers0 INTERFACE include)
target_link_libraries(demo7 PRIVATE my_headers0)
target_link_libraries(my_test_7_test PRIVATE my_headers0)
# begin dependencies from cxxdeps.txt
# cxxdeps dependency ut
FetchContent_Declare(ut GIT_REPOSITORY https://github.com/boost-ext/ut GIT_TAG v2.3.1)
FetchContent_MakeAvailable(ut)
target_link_libraries(my_test_7_test PRIVATE Boost::ut)
# finally, add all sources
set(SOURCES
)
target_sources(demo7 PRIVATE ${SOURCES})
target_sources(my_test_7_test PRIVATE ${SOURCES})