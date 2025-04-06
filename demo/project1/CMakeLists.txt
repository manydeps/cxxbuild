cmake_minimum_required(VERSION 4.0)
project(my-project LANGUAGES CXX VERSION 0.0.1)
set (CMAKE_CXX_STANDARD 17)
set (CMAKE_CXX_STANDARD_REQUIRED ON)
set (CMAKE_CXX_EXTENSIONS OFF)
set (CMAKE_EXPORT_COMPILE_COMMANDS ON)
Include(FetchContent)
# add all executables
add_executable(demo1 src/demo1.cpp )
add_executable(my_test tests/my_test.cpp )
add_library(my_headers0 INTERFACE)
target_include_directories(my_headers0 INTERFACE include)
target_link_libraries(demo1 PRIVATE my_headers0)
target_link_libraries(my_test PRIVATE my_headers0)
# begin dependencies from cxxdeps.txt
# cxxdeps dependency fmt
FetchContent_Declare(fmt GIT_REPOSITORY https://github.com/fmtlib/fmt.git GIT_TAG 9.1.0)
FetchContent_MakeAvailable(fmt)
target_link_libraries(my_headers0 INTERFACE fmt)
target_link_libraries(demo1 PRIVATE fmt)
target_link_libraries(my_test PRIVATE fmt)
# cxxdeps dependency fmt
# cxxdeps dependency Catch2
FetchContent_Declare(Catch2 GIT_REPOSITORY https://github.com/catchorg/Catch2.git GIT_TAG v3.5.1)
FetchContent_MakeAvailable(Catch2)
target_link_libraries(my_test PRIVATE Catch2::Catch2WithMain)
# cxxdeps dependency catch2
# cxxdeps dependency pthread
# system dependency: -lpthread
IF (NOT WIN32) # !windows
target_link_libraries(my_headers0 INTERFACE pthread)
target_link_libraries(demo1 PRIVATE pthread)
target_link_libraries(my_test PRIVATE pthread)
ENDIF()
# cxxdeps dependency crypto
# system dependency: -lcrypto
IF (UNIX AND NOT APPLE) # linux
target_link_libraries(my_headers0 INTERFACE crypto)
target_link_libraries(demo1 PRIVATE crypto)
target_link_libraries(my_test PRIVATE crypto)
ENDIF()
# finally, add all sources
set(SOURCES
	src/something.cpp
)
target_sources(demo1 PRIVATE ${SOURCES})
target_sources(my_test PRIVATE ${SOURCES})