cmake_minimum_required(VERSION 4.0)
project(my-project LANGUAGES CXX VERSION 0.0.1)
set (CMAKE_CXX_STANDARD 20)
set (CMAKE_CXX_STANDARD_REQUIRED ON)
set (CMAKE_CXX_EXTENSIONS OFF)
set (CMAKE_EXPORT_COMPILE_COMMANDS ON)
Include(FetchContent)
add_definitions(-DMY_HELLO="ola mundo")
add_definitions(-DIS_TEST)
# add all executables
add_executable(demo6 src/demo6.cpp )    # main
add_library(my_headers0 INTERFACE)
target_include_directories(my_headers0 INTERFACE inc)
target_link_libraries(demo6 PRIVATE my_headers0)
# begin dependencies from cxxdeps.txt
# cxxdeps dependency absl
FetchContent_Declare(absl GIT_REPOSITORY https://github.com/abseil/abseil-cpp.git GIT_TAG 20240116.1)
FetchContent_MakeAvailable(absl)
target_link_libraries(my_headers0 INTERFACE absl::base)
target_link_libraries(my_headers0 INTERFACE absl::synchronization)
target_link_libraries(my_headers0 INTERFACE absl::strings)
target_link_libraries(my_headers0 INTERFACE absl::log)
target_link_libraries(my_headers0 INTERFACE absl::log_initialize)
target_link_libraries(demo6 PRIVATE absl::base)
target_link_libraries(demo6 PRIVATE absl::synchronization)
target_link_libraries(demo6 PRIVATE absl::strings)
target_link_libraries(demo6 PRIVATE absl::log)
target_link_libraries(demo6 PRIVATE absl::log_initialize)
# cxxdeps dependency OptFrame
set(OptFrame_DIR "${CMAKE_SOURCE_DIR}/./thirdparty/optframe-master/cmake/")
find_package(OptFrame REQUIRED)
include_directories("${OptFrame_INCLUDE_DIRS}")
# finally, add all sources
set(SOURCES
	src/demo6.cpp
	src/demo6.cpp
)
target_sources(demo6 PRIVATE ${SOURCES})