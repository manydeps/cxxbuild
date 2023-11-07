#!/usr/bin/env python3

# MIT License
# Copyleft 2023 Igor Machado Coelho

"""
	Usage:
       cxxbuild [ROOT_FOLDER] => example: cxxbuild .
       cxxbuild lint => TODO: will invoke linter
       cxxbuild clean => TODO: will clean
       cxxbuild test => TODO: will invoke tests
       MORE BUILD OPTIONS:
       * c++11 => TODO: use c++11 standard
       * bazel => TODO: use bazel build system (instead of cmake)

       SEE ALSO cxxdeps.txt FILE:
       fmt == "9.1.0"     [ fmt ]                    git *    https://github.com/fmtlib/fmt.git
       Catch2 == "v3.3.1" [ Catch2::Catch2WithMain ] git test https://github.com/catchorg/Catch2.git  special_catch_cmake_extras
       m

"""

import os
import sys
import json
import subprocess

print("======================================")
print("         welcome to cxxbuild          ")
print("======================================")

# ASSUME '.' as root_path if nothing is passed
if len(sys.argv) == 1:
    sys.argv.append(".")

# clean deletes all files matching CLEAN_EXT
if "clean" in sys.argv:
    print("'clean' not implemented, yet!")
    exit()
if "lint" in sys.argv:
    print("'lint' not implemented, yet!")
    exit()
 
root_path = sys.argv[1]

print("begin build on root_path=",root_path)
# find all source files,
# find all files with an entry point,
src_list = []
src_main = {}
# ENFORCING THIS PATH... MUST ADD MULTIPLE PATH OPTION!
# src_paths = [root_path, root_path+"/src"] 
src_paths = [root_path+"/src"] 
print("src_paths=", src_paths)
entrypoint = "main("  # Pattern to find main(), or main(int argc, ...), etc
#
src_ext = ['.c', '.cc', '.cpp', '.cxx', '.c++']
print(src_ext)
for src_path in src_paths:
    for root, subdirs, files in os.walk(src_path):
        root = root.removeprefix(root_path).removeprefix("/")
        print("root_SRC: ", root)
        print("subdirs_SRC: ", subdirs)
        print("files_SRC: ", files)
        for file in files:
            file_name, ext = os.path.splitext(file)
            if ext in src_ext:
                file_path = os.path.join(root, file)
                src_list.append(file_path)
                with open(root_path+"/"+file_path, 'r') as fd:
                    # TODO: add other formats for main... such as "int main()", etc...
                    # ANYWAY, these limitations are acceptable! 
                    # other options are: " main(" and "\nmain("
                    # If someone has a function "xxxmain(" it can currently break.
                    entrypoint = "main("
                    print("checking entrypoint:", entrypoint)
                    if entrypoint in fd.read():
                        src_main[file_path] = (root, file_name)
    # end-for src_path
# end-for src_paths

print("src_main:", src_main)
print("src_list:", src_list)

# finding tests...

src_test_list = []
src_test_main = {}
src_test_nomain = {}
#
print(src_ext)
for root, subdirs, files in os.walk(root_path+"/tests"):
    root = root.removeprefix(root_path).removeprefix("/")
    print("TEST root: ", root)
    print("TEST subdirs: ", subdirs)
    print("TEST files: ", files)
    for file in files:
        file_name, ext = os.path.splitext(file)
        if ext in src_ext:
            file_path = os.path.join(root, file)
            src_test_list.append(file_path)
            src_test_nomain[file_path] = (root, file_name)
            with open(root_path+"/"+file_path, 'r') as fd:
                # TODO: add other formats for main... such as "int main()", etc...
                # ANYWAY, these limitations are acceptable! 
                # other options are: " main(" and "\nmain("
                # If someone has a function "xxxmain(" it can currently break.
                entrypoint = "main("
                print("checking entrypoint:", entrypoint)
                if entrypoint in fd.read():
                    src_test_main[file_path] = (root, file_name+"_test")

print("src_test_main:", src_test_main)
print("src_test_nomain:", src_test_nomain)
print("src_test_list:", src_test_list)

# SO... TIME TO FIND INCLUDE FOLDERS

INCLUDE_DIRS = []
for root, subdirs, files in os.walk(root_path):
    root = root.removeprefix(root_path).removeprefix("/")
    #print("root: ", root)
    #print("subdirs: ", subdirs)
    #print("files: ", files)
    if "include" in subdirs:
        incdir = root+"/include"
        incdir = incdir.removeprefix(root_path).removeprefix("/")
        INCLUDE_DIRS.append(incdir)
    # TODO: search in other places too... maybe inside src?

print("INCLUDE_DIRS=",INCLUDE_DIRS)

# READ cxxdeps.txt file, if available...
# AT THIS POINT, ASSUMING 'cmake' OPTION (NO 'bazel' FOR NOW!)
cmakelists = []
cmakelists.append("cmake_minimum_required(VERSION 3.27)")
cmakelists.append("project(my-project LANGUAGES CXX VERSION 0.0.1)")
# TODO: get 'c++20' parameter and use it, if necessary.
# Standard C++ is c++17, for now! Always adopt ONE LESS the current one (c++20)!
cmakelists.append("set (CMAKE_CXX_STANDARD 20)") # TODO: make it 17
cmakelists.append("set (CMAKE_CXX_STANDARD_REQUIRED ON)")
cmakelists.append("set (CMAKE_CXX_EXTENSIONS OFF)")
cmakelists.append("set (CMAKE_EXPORT_COMPILE_COMMANDS ON)")
cmakelists.append("Include(FetchContent)")
# add_executable for binaries
for filepath, app_name in src_main.items():
    cmakelists.append("add_executable("+app_name[1]+" "+filepath+")")
# add_executable for test binaries
print("finding test executables!")
# if no main is found, then each test is assumed to be independent!
if len(src_test_main.items()) == 0:
    print("WARNING: no main() is found for tests... using main-less strategy!")
    src_test_main = src_test_nomain
for filepath, app_name in src_test_main.items():
    cmakelists.append("add_executable("+app_name[1]+" "+filepath+")")


# INCLUDE_DIRS will act as header-only libraries
#  => DO NOT ADD SOURCE FILES INTO include FOLDERS!!!
for i in range(len(INCLUDE_DIRS)):
    cmakelists.append("add_library(my_headers"+str(i)+" INTERFACE)")
    cmakelists.append("target_include_directories(my_headers"+str(i)+" INTERFACE "+INCLUDE_DIRS[i]+"/)")
    for filepath, app_name in src_main.items():
        cmakelists.append("target_link_libraries("+app_name[1]+" PRIVATE my_headers"+str(i)+")")    
    for filepath, app_name in src_test_main.items():
        cmakelists.append("target_link_libraries("+app_name[1]+" PRIVATE my_headers"+str(i)+")")    
#
#print(cmakelists)

with open(root_path+'/cxxdeps.txt', 'r') as fd:
    x=fd.readlines()
    #print(x)
    cmakelists.append("# begin dependencies from cxxdeps.txt")
    for l in x:
        if (len(l) >= 1) and (l[0] != '#'):
            # good line!
            print(l)
            fields = l.split()
            print(fields)
            # assume all spacing is correct, for now!
            if len(fields) == 0:
                # IGNORE (EMPTY LINE!)
                continue
            project_name = fields[0]
            cmakelists.append("# cxxdeps dependency "+project_name)
            if len(fields) == 1:
                # SYSTEM STATIC LIBRARY! example: -lm
                # MANUALLY PUSH STANDARD PARAMETERS: m == * [ m ] system *
                fields.append('==')
                fields.append('*')
                fields.append('[')
                fields.append(project_name)
                fields.append(']')
                fields.append('system')
                fields.append('*')
            # expects '==' now!
            assert(fields[1] == "==")
            version_number = fields[2].strip('"')
            if len(fields) == 3:
                # SYSTEM STATIC LIBRARY WITH VERSION! example: -lm=0.0.0
                # DON'T DOING THIS NOW...
                print("WARNING: ignoring system library WITH VERSION: "+project_name)
                assert(False)
                continue
            # begin reading library list
            assert fields[3] == '['
            libs = []
            k = 4
            next_lib = fields[k]
            while next_lib != ']':
                libs.append(next_lib)
                k = k + 1
                next_lib = fields[k]
            # finished parsing libs list
            assert fields[k] == ']'
            k = k+1
            # MUST HAVE A pkg_manager and mode (simplifying this for now...)
            pkg_manager = fields[k]
            mode = fields[k+1]
            k = k+2
            if pkg_manager == 'system':
                # AT THIS POINT, SYSTEM LIBRARY MUST HAVE ITS LIB INSIDE, example: ['m']
                cmakelists.append('# system dependency: -l'+project_name)
                if mode == '*':
                    for i in range(len(INCLUDE_DIRS)):
                        for l in libs:
                            cmakelists.append("target_link_libraries(my_headers"+str(i)+" INTERFACE "+project_name+")")
                    for filepath, app_name in src_main.items():
                        for l in libs:
                            cmakelists.append("target_link_libraries("+app_name[1]+" PRIVATE "+project_name+")")    
                    for filepath, app_name in src_test_main.items():
                        for l in libs:
                            cmakelists.append("target_link_libraries("+app_name[1]+" PRIVATE "+project_name+")")    
                # end-if *
                # attach it to test binaries, if mode is 'test'
                if mode == 'test':
                    for filepath, app_name in src_test_main.items():
                        for l in libs:
                            cmakelists.append("target_link_libraries("+app_name[1]+" PRIVATE "+project_name+")")    
                # end-if test
                continue
            #end-if system
            if pkg_manager == 'git':
                git_url = fields[k]
                k=k+1
            cmakelists.append("FetchContent_Declare("+project_name+" GIT_REPOSITORY "+git_url+" GIT_TAG "+version_number+")")
            cmakelists.append("FetchContent_MakeAvailable("+project_name+")")
            # attach it to libraries, binaries and test binaries, if mode is *
            if mode == '*':
                for i in range(len(INCLUDE_DIRS)):
                    for l in libs:
                        cmakelists.append("target_link_libraries(my_headers"+str(i)+" INTERFACE "+l+")")
                for filepath, app_name in src_main.items():
                    for l in libs:
                        cmakelists.append("target_link_libraries("+app_name[1]+" PRIVATE "+l+")")    
                for filepath, app_name in src_test_main.items():
                    for l in libs:
                        cmakelists.append("target_link_libraries("+app_name[1]+" PRIVATE "+l+")")    
            # attach it to test binaries, if mode is 'test'
            if mode == 'test':
                for filepath, app_name in src_test_main.items():
                    for l in libs:
                        cmakelists.append("target_link_libraries("+app_name[1]+" PRIVATE "+l+")")    
            # read special, if exists
            print("k=",k)
            if k < len(fields):
                special = fields[k]
                k = k+1
                print("special=",special)
                # IGNORING THE special part for now... or forever, I hope!!!
                if special == '_special_catch_cmake_extras':
                    cmakelists.append("list(APPEND CMAKE_MODULE_PATH ${catch2_SOURCE_DIR}/extras)")    
                    cmakelists.append("include(CTest)")
                    cmakelists.append("include(Catch)")
                    for filepath, app_name in src_test_main.items():
                        cmakelists.append("catch_discover_tests("+app_name[1]+")")    
            # end special
        # end if not comment
    # end for line
# end cxxdeps

# Generate CMakeLists.txt (or look for other option, such as 'bazel')
# Assuming CMake and Ninja for now (TODO: must detect and warn to install!)

# TODO: check if some CMakeLists.txt exists before overwriting it!
# TODO: make backup of CMakeLists.txt only if content is different...

# ============ create CMakeLists.txt ===========
with open(root_path+'/CMakeLists.txt', 'w') as file:
    file.write('\n'.join(cmakelists))

print("-----------------------------------")
print("CMakeLists.txt generated on folder:")
print(" => "+root_path+'/CMakeLists.txt')
print("-----------------------------------")

# ============ build with cmake+ninja ===========
# STEP 1: check that 'cmake' and 'ninja' command exists
CHECK_CMAKE_CMD="cmake --version"
print("Please install latest cmake with: python3 -m pip install cmake --upgrade")
print("or visit cmake website: https://cmake.org/download/")
print("checking cmake command now...")
x=subprocess.call(list(filter(None, CHECK_CMAKE_CMD.split(' '))))
print('check result:', x)
assert(x == 0)
#
CHECK_NINJA_CMD="ninja --version"
print("Please install latest ninja:")
print(" * on linux/ubuntu with apt: apt-get install ninja-build")
print(" * on mac with homebrew: brew install ninja")
print(" * on windows with chocolatey: choco install ninja")
print("or visit ninja website: https://ninja-build.org/")
print("checking ninja command now...")
x=subprocess.call(list(filter(None, CHECK_NINJA_CMD.split(' '))))
print('check result:', x)
assert(x == 0)
#
# STEP 2: build with cmake+ninja
CMAKE_CMD="cmake -B"+root_path+"/build -S"+root_path+" -GNinja"
NINJA_CMD="ninja -C "+root_path+"/build"
print("building... "+CMAKE_CMD)
x=subprocess.call(list(filter(None, CMAKE_CMD.split(' '))))
print('cmake result:', x)
assert(x == 0)
x=subprocess.call(list(filter(None, NINJA_CMD.split(' '))))
print('ninja result:', x)
assert(x == 0)
