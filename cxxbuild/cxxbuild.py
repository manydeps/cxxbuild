#!/usr/bin/env python3

# MIT License
# Copyleft 2023 Igor Machado Coelho

import os
import sys
import json
import subprocess


def usage():
    u="""
cxxbuild=1.3.9
Usage:
    cxxbuild [build] [ROOT_PATH] 
      builds with cxxbuild, examples: 
        cxxbuild
        cxxbuild .
        cxxbuild build .
    cxxbuild help
      displays usage()
    cxxbuild lint => TODO: will invoke linter
    cxxbuild clean => TODO: will clean
    cxxbuild test => TODO: will invoke tests
    FLAGS:
       --src SRC_PATH 
            * sets source folder (default: src) 
       --tests TESTS_PATH 
            * sets tests folder (default: tests) 
       --include INCLUDE_PATH 
            * sets include folder (default: include) 
    MORE BUILD OPTIONS:
       * c++11 => TODO: use c++11 standard
       * bazel => TODO: use bazel build system (instead of cmake)

    SEE ALSO cxxdeps.txt FILE:
        fmt == "9.1.0"     [ fmt ]                    git *    https://github.com/fmtlib/fmt.git
        Catch2 == "v3.3.1" [ Catch2::Catch2WithMain ] git test https://github.com/catchorg/Catch2.git
        m
    """
    print(u)

def get_cmakelists_from_cxxdeps(root_path, cmakelists, INCLUDE_DIRS, src_main, src_test_main):
    try:
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
                    project_name_full = fields[0]
                    lproj = project_name_full.split(":")
                    project_name = project_name_full.split(":")[0]
                    triplet = ""
                    not_triplet = False
                    if len(lproj) > 1:
                        triplet = project_name_full.split(":")[1]
                        if triplet.startswith("!"):
                            not_triplet = True
                            triplet = triplet[1:]  # remove "!"
                    #
                    import platform
                    my_system = platform.system()
                    #
                    print("PROJECT:", project_name, " TRIPLET:", triplet, "SYSTEM:", my_system)
                    #
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
                        # SYSTEM STATIC LIBRARY WITH VERSION! example: -lm=0.0.1
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
                        if triplet != "":
                            cmakelists.append(make_if_triplet(triplet, not_triplet, my_system))        
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
                        if triplet != "":
                            cmakelists.append("ENDIF()")
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

    except FileNotFoundError:
        print("File cxxdeps.txt does not exist... ignoring it!")

    return cmakelists

def get_toml_dep(dep_name, section_name, dep_object):
    print("get_toml_dep(...) dep_name: ", dep_name, " section:", section_name, " dep_object:", dep_object)
    local_dep = []
    triplet=""
    for x1, y1 in dep_object.items():
        if x1 == "triplet":
            triplet = y1
    if triplet != "":
        dep_name = dep_name + ":" + triplet
    local_dep.append(dep_name)
    version = "*"
    for x1, y1 in dep_object.items():
        if x1 == "version":
            version = "\""+y1+"\""
    # read links and packages part
    list_part = []
    list_part.append("[")
    dep_type = ""
    for x1, y1 in dep_object.items():
        if x1 == "links" or x1 == "pip" or x1 == "choco" or x1 == "apt" or x1 == "npm":
            if x1 != "links":
                dep_type = x1 
            for d in y1:
                list_part.append(d)
    list_part.append("]")
    # check dep type and complement part
    complement = ""
    if dep_type == "":
        for x1, y1 in dep_object.items():
            if x1 == "git":
                dep_type = "git"
                complement = y1
                for x2, y2 in dep_object.items():
                    if x2 == "tag":
                        version = "\""+y2+"\""
    if dep_type == "":
        dep_type = "system" # assuming 'system' as default
    #
    if dep_type == "system" and len(list_part) == 2 and section_name == "all":
        # do nothing... list is '[ ]'
        return local_dep
    # fill general data
    local_dep.append("==")
    local_dep.append(version)
    local_dep += list_part
    local_dep.append(dep_type)
    if section_name != "all":
        local_dep.append(section_name)
    else:
        local_dep.append("*")
    if complement != "":
        local_dep.append(complement)

    return local_dep

# triplet can be "linux", "windows", "osx"
# not_triplet can be False of True (if negated).. e.g., "!windows"
def make_if_triplet(triplet, not_triplet, my_system):
    assert(triplet != "")
    striplet = "IF ("
    if triplet == "windows":
        if not_triplet:
            striplet += "NOT WIN32) # !windows"
        else:
            striplet += "WIN32) # windows"
        return striplet
    if triplet == "linux":
        if not_triplet:
            striplet += "NOT UNIX OR APPLE) # !linux"
        else:
            striplet += "UNIX AND NOT APPLE) # linux"
        return striplet
    if triplet == "osx":
        if not_triplet:
            striplet += "NOT APPLE OR NOT CMAKE_SYSTEM_NAME STREQUAL \"Darwin\") # !osx"
        else:
            striplet += "APPLE AND CMAKE_SYSTEM_NAME STREQUAL \"Darwin\") # osx"
        return striplet
    assert(False)
    return ""

# detect if it's 'cmd' for windows, but not 'bash'
def is_cmd():
    return os.name == 'nt' and 'WSL_DISTRO_NAME' not in os.environ


def main():
    print("======================================")
    print("         welcome to cxxbuild          ")
    print("======================================")

    # ASSUME '.' as root_path if nothing is passed
    if len(sys.argv) == 1:
        sys.argv.append(".")

    if "help" in sys.argv:
        usage()
        exit()
    # clean deletes all files matching CLEAN_EXT
    if "clean" in sys.argv:
        print("'clean' not implemented, yet!")
        exit()
    if "lint" in sys.argv:
        print("'lint' not implemented, yet!")
        exit()
    root_path = sys.argv[1]
    if "build" in sys.argv:
        # must take path explicitly from third argument!
        # example: cxxbuild build .
        if len(sys.argv) > 2:
            root_path = sys.argv[2]
        else:
            usage()
            exit()

    search_src="src"
    search_tests="tests"
    search_include="include"
    for i in range(len(sys.argv)):
        if (sys.argv[i] == "--src"):
            search_src = str(sys.argv[i + 1])
        if (sys.argv[i] == "--tests"):
            search_tests = str(sys.argv[i + 1])
        if (sys.argv[i] == "--include"):
            search_include = str(sys.argv[i + 1])

    #
    print("begin build on root_path=",root_path)
    # find all source files,
    # find all files with an entry point,
    src_list = []
    src_main = {}
    # ENFORCING THIS PATH... MUST ADD MULTIPLE PATH OPTION!
    # src_paths = [root_path, root_path+"/src"] 
    src_paths = [root_path+"/"+search_src] 
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
    for root, subdirs, files in os.walk(root_path+"/"+search_tests):
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
            incdir = root+"/"+search_include
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
    # add sources!
    cmakelists.append("set(SOURCES")
    for f in src_list:
        for filepath, app_name in src_main.items():
            filepath2 = filepath.replace("\\", "/")
            f2 = f.replace("\\", "/")
            if filepath2 != f2:
                cmakelists.append("\t"+f2)
    cmakelists.append(")")
    # add_executable for binaries
    for filepath, app_name in src_main.items():
        cmakelists.append("add_executable("+app_name[1]+" "+filepath.replace("\\", "/")+" ${SOURCES})")
    # add_executable for test binaries
    print("finding test executables!")
    # if no main is found, then each test is assumed to be independent!
    if len(src_test_main.items()) == 0:
        print("WARNING: no main() is found for tests... using main-less strategy!")
        src_test_main = src_test_nomain
    for filepath, app_name in src_test_main.items():
        cmakelists.append("add_executable("+app_name[1]+" "+filepath.replace("\\", "/")+" ${SOURCES})")


    # INCLUDE_DIRS will act as header-only libraries
    #  => DO NOT ADD SOURCE FILES INTO include FOLDERS!!!
    for i in range(len(INCLUDE_DIRS)):
        cmakelists.append("add_library(my_headers"+str(i)+" INTERFACE)")
        cmakelists.append("target_include_directories(my_headers"+str(i)+" INTERFACE "+INCLUDE_DIRS[i]+")")
        for filepath, app_name in src_main.items():
            cmakelists.append("target_link_libraries("+app_name[1]+" PRIVATE my_headers"+str(i)+")")    
        for filepath, app_name in src_test_main.items():
            cmakelists.append("target_link_libraries("+app_name[1]+" PRIVATE my_headers"+str(i)+")")    
    #
    #print(cmakelists)

    try:
        cxxdeps_all = []
        cxxdeps_test = []
        cxxdeps_dev = []
        with open(root_path+'/cxxdeps.toml', 'r') as toml_file:
            import toml
            data = toml.load(toml_file)
            #
            for section_name, section_data in data.items():
                print(f"SECTION=[{section_name}]")
                # Iterate over dependencies within each section
                for dependency_name, dependency_info in section_data.items():
                    print("processing dependency: ", dependency_name)
                    #print(f"BEGIN {dependency_name}={dependency_info} END")
                    if isinstance(dependency_info, list):
                        #print("Dependency LIST... checking triplets!")
                        for d in dependency_info:
                            #print("d:",d)
                            x = get_toml_dep(dependency_name, section_name, d)
                            if section_name == "test":
                                cxxdeps_test.append(x)
                            elif section_name == "dev":
                                cxxdeps_dev.append(x)
                            else:
                                cxxdeps_all.append(x)
                        #print("END Dependency LIST")
                    elif isinstance(dependency_info, dict):
                        #print("Dependency DICT")
                        x = get_toml_dep(dependency_name, section_name, dependency_info)
                        if section_name == "test":
                            cxxdeps_test.append(x)
                        elif section_name == "dev":
                            cxxdeps_dev.append(x)
                        else:
                            cxxdeps_all.append(x)
                    else:
                        print("Dependency info is neither a list nor an object.")
                        assert(False)
                print("\n")
        # end with
        # finishing .toml file
        print("cxxdeps_all:", cxxdeps_all)
        print("cxxdeps_test:", cxxdeps_test)
        print("cxxdeps_dev:", cxxdeps_dev)
        # writing cxxdeps.txt and cxxdeps.dev.txt
        if len(cxxdeps_dev) > 0:
            with open(root_path+"/cxxdeps.dev.txt", "w") as output_file:
                output_file.write("# DO NOT EDIT! file 'cxxdeps.dev.txt' generated automatically from 'cxxdeps.toml'" + "\n")
                for dep in cxxdeps_dev:
                    output_file.write(" ".join(dep) + "\n")
        if len(cxxdeps_all) > 0 or len(cxxdeps_test) > 0:
            with open(root_path+"/cxxdeps.txt", "w") as output_file:
                output_file.write("# DO NOT EDIT! file 'cxxdeps.txt' generated automatically from 'cxxdeps.toml'" + "\n")
                for dep in cxxdeps_all:
                    output_file.write(" ".join(dep) + "\n")
                for dep in cxxdeps_test:
                    output_file.write(" ".join(dep) + "\n")
            
    except FileNotFoundError:
        print("File cxxdeps.toml does not exist... ignoring it!")

    # cxxdeps.txt
    cmakelists = get_cmakelists_from_cxxdeps(root_path, cmakelists, INCLUDE_DIRS, src_main, src_test_main)



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
    # STEP 1.5: debug only (TODO: create flag --verbose!)
    CMAKE_CMD="cat "+root_path+"/CMakeLists.txt"
    print("showing CMakeLists.txt... "+CMAKE_CMD)
    x=subprocess.call(list(filter(None, CMAKE_CMD.split(' '))))
    print('cmake result:', x)
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

    if len(src_main.items()) > 0:
        print("OK: at least one main() has been found!")
    else:
        print("WARNING: no main() has been found!")

if __name__ == '__main__':
    main()