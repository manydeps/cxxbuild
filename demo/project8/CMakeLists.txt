cmake_minimum_required(VERSION 4.0)
set (CMAKE_CXX_COMPILER /usr/bin/clang++-19)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -stdlib=libc++")
set(CMAKE_EXPERIMENTAL_CXX_IMPORT_STD "a9e1cf81-9932-4810-974b-6eccaf14e457")
set(CMAKE_CXX_MODULE_STD 1)
project(my-project LANGUAGES CXX VERSION 0.0.1)
set (CMAKE_CXX_STANDARD 23)
set (CMAKE_CXX_STANDARD_REQUIRED ON)
set (CMAKE_CXX_EXTENSIONS ON)
set (CMAKE_EXPORT_COMPILE_COMMANDS ON)
Include(FetchContent)
set(BOOST_UT_DISABLE_MODULE OFF)
# add all executables
add_library(get_data_cpp23 )   # cxx module: get_data_cpp23
target_sources(get_data_cpp23 PUBLIC  FILE_SET CXX_MODULES FILES src/lista01/get_data_cpp23.cppm)
add_executable(demo8 src/demo8.cpp )    # main
target_link_libraries(demo8  get_data_cpp23 )
add_executable(my_test_8_test tests/my_test_8.cpp )
target_link_libraries(my_test_8_test PRIVATE  get_data_cpp23 )
# begin dependencies from cxxdeps.txt
# cxxdeps dependency ut
FetchContent_Declare(ut GIT_REPOSITORY https://github.com/boost-ext/ut GIT_TAG v2.3.1)
FetchContent_MakeAvailable(ut)
target_link_libraries(my_test_8_test PRIVATE Boost::ut_module)
# finally, add all sources
set(SOURCES
)
target_sources(demo8 PRIVATE ${SOURCES})
target_sources(my_test_8_test PRIVATE ${SOURCES})