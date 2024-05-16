cmake_minimum_required(VERSION 3.27)
project(my-project LANGUAGES CXX VERSION 0.0.1)
set (CMAKE_CXX_STANDARD 20)
set (CMAKE_CXX_STANDARD_REQUIRED ON)
set (CMAKE_CXX_EXTENSIONS OFF)
set (CMAKE_EXPORT_COMPILE_COMMANDS ON)
Include(FetchContent)
set(SOURCES
)
add_executable(demo6 src/demo6.cpp ${SOURCES})
# begin dependencies from cxxdeps.txt
# cxxdeps dependency absl
FetchContent_Declare(absl GIT_REPOSITORY https://github.com/abseil/abseil-cpp.git GIT_TAG 20240116.1)
FetchContent_MakeAvailable(absl)
target_link_libraries(demo6 PRIVATE absl::base)
target_link_libraries(demo6 PRIVATE absl::synchronization)
target_link_libraries(demo6 PRIVATE absl::strings)
target_link_libraries(demo6 PRIVATE absl::log)
target_link_libraries(demo6 PRIVATE absl::log_initialize)
# cxxdeps dependency optframe
FetchContent_Declare(optframe GIT_REPOSITORY https://github.com/optframe/optframe.git GIT_TAG master)
FetchContent_MakeAvailable(optframe)
target_link_libraries(demo6 PRIVATE OptFrameAll)