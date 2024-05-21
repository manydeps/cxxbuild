cmake_minimum_required(VERSION 3.27)
project(my-project LANGUAGES CXX VERSION 0.0.1)
set (CMAKE_CXX_STANDARD 20)
set (CMAKE_CXX_STANDARD_REQUIRED ON)
set (CMAKE_CXX_EXTENSIONS OFF)
set (CMAKE_EXPORT_COMPILE_COMMANDS ON)
Include(FetchContent)
# add all executables
add_executable(demo4 src/demo4.cpp )
add_executable(my_test tests/my_test.cpp )
add_library(my_headers0 INTERFACE)
target_include_directories(my_headers0 INTERFACE include)
target_link_libraries(demo4 PRIVATE my_headers0)
target_link_libraries(my_test PRIVATE my_headers0)
# begin dependencies from cxxdeps.txt
# cxxdeps dependency Catch2
FetchContent_Declare(Catch2 GIT_REPOSITORY https://github.com/catchorg/Catch2.git GIT_TAG v3.5.1)
FetchContent_MakeAvailable(Catch2)
target_link_libraries(my_test PRIVATE Catch2::Catch2WithMain)
# cxxdeps dependency catch2
# finally, add all sources
set(SOURCES
	src/something.cpp
)
target_sources(demo4 PRIVATE ${SOURCES})
target_sources(my_test PRIVATE ${SOURCES})