#!/usr/bin/env python3

# MIT License
# Copyleft 2025 Igor Machado Coelho

# /// script
# requires-python = ">=3.9"
# dependencies = ["toml", "packaging"]
# ///

import os
import platform
import sys
import subprocess

# process begin on: def main()

def version():
    v = "cxxbuild=1.7.0"
    return v

def usage():
    u=version()+"""
Usage:
    cxxbuild [build] [ROOT_PATH] 
      builds with cxxbuild, examples: 
        cxxbuild
        cxxbuild .
        cxxbuild build .
        cxxbuild . --c++20 --bazel
    cxxbuild help
      displays this usage message and available options
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
       * --c++11 => use c++11 standard
       * --c++14 => use c++14 standard
       * --c++17 => use c++17 standard (DEFAULT)
       * --c++20 => use c++20 standard
       * --c++23 => use c++23 standard
       * --gnu++23 => use c++23 extensions
       * --c++26 => use c++26 standard
       * --cmake => use cmake build system (DEFAULT)
       * --bazel => use bazel build system (instead of cmake)

    SEE ALSO cxxdeps.txt FILE:
        fmt == "9.1.0"     [ fmt ]                    git *    https://github.com/fmtlib/fmt.git
        Catch2 == "v3.3.1" [ Catch2::Catch2WithMain ] git test https://github.com/catchorg/Catch2.git
        m
    """
    print(u)

def get_cmakelists_from_cxxdeps(VERBOSE, root_path, cmakelists, INCLUDE_DIRS, src_main, src_test_main):
    import platform
    my_system = platform.system()
    print("cxxbuild: get_cmakelists_from_cxxdeps on platform =", my_system)
    x = []
    found = False
    if my_system == "Windows":
        try:
            with open(root_path+'/cxxdeps.windows.txt', 'r') as fd:
                x=fd.readlines()
                print("cxxbuild: found 'cxxdeps.windows.txt'...")
                found = True
        except FileNotFoundError:
            if VERBOSE:
                print("cxxbuild cmake: File cxxdeps.windows.txt does not exist... ignoring it!")
    if not found:
        try:
            with open(root_path+'/cxxdeps.txt', 'r') as fd:
                x=fd.readlines()
                print("cxxbuild: found 'cxxdeps.txt'...")
        except FileNotFoundError:
            if VERBOSE:
                print("cxxbuild cmake: File cxxdeps.txt does not exist... ignoring it!")
    if len(x) > 0:
        #print(x)
        cmakelists.append("# begin dependencies from cxxdeps.txt")
        for l in x:
            if (len(l) >= 1) and (l[0] != '#') and (l[0] != '!'):
                # good line!
                if VERBOSE:
                    print(l)
                fields = l.split()
                if VERBOSE:
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
                print("cxxdeps cmake PROJECT:", project_name, " TRIPLET:", triplet, "SYSTEM:", my_system)
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
                if pkg_manager[0:6] == 'bazel+':
                    print("WARNING: ignoring 'bazel+' entry for CMAKE: "+project_name)
                    continue
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
                elif pkg_manager == 'git' or pkg_manager == 'cmake+git':
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
                    if VERBOSE:
                        print("k=",k)
                    if k < len(fields):
                        special = fields[k]
                        k = k+1
                        if VERBOSE:
                            print("special=",special)
                        # IGNORING THE special part for now... or forever, I hope!!!
                        if special == '_special_catch_cmake_extras':
                            cmakelists.append("list(APPEND CMAKE_MODULE_PATH ${catch2_SOURCE_DIR}/extras)")    
                            cmakelists.append("include(CTest)")
                            cmakelists.append("include(Catch)")
                            for filepath, app_name in src_test_main.items():
                                cmakelists.append("catch_discover_tests("+app_name[1]+")")    
                    # end special
                    continue
                # end if git
                elif pkg_manager == 'local' or pkg_manager == 'cmake+local':
                    # on cmake, this is resolved using find_package module
                    local_path = fields[k]
                    # check if local path is empty
                    if local_path == "_":
                        local_path = ""
                    k=k+1
                    # check if including libraries and special fix/patch
                    add_inc_lib = True
                    special = ""
                    if k < len(fields):
                        add_inc_lib = fields[k]
                        if add_inc_lib == "true" or add_inc_lib == "True":
                            add_inc_lib = True
                        else:
                            add_inc_lib = False
                        k = k+1
                        if k < len(fields):
                            special = fields[k]
                            k = k+1
                    # begin construction of FindPackage
                    if local_path != "":
                        cmakelists.append("set("+project_name+"_DIR \"${CMAKE_SOURCE_DIR}/"+local_path+"\")")
                    # ignoring 'version_number', for now!
                    cmakelists.append("find_package("+project_name+" REQUIRED)")
                    if add_inc_lib:
                        cmakelists.append("include_directories(\"${"+project_name+"_INCLUDE_DIRS}\")")
                        # todo: check libraries as well
                    # todo: attach it to libraries, binaries and test binaries, if mode is *
                    if special != "":
                        # load patch file and append it
                        with open(root_path+'/'+special, 'r') as fdx:
                            patches=fdx.readlines()
                            for p_line in patches:
                                cmakelists.append(p_line)
                    continue
                # end if local
                print("cxxdeps error: build type '"+pkg_manager+"' unknown or not supported!")
                exit(1)
            # end if not comment
        # end for line
    # end cxxdeps

    return cmakelists

class BazelFiles:
    def __init__(self):
        self.MODULE = []
        self.bazelrc = []
        self.BUILD_root = []
        self.BUILD_tests = []
        # helpers
        self.targets_main = []
        self.targets_tests = []
        self.targets_include = []
        self.cxxopt_windows = []
        self.cxxopt_linux = []
        self.cxxopt_macos = []

def get_bazelfiles_from_cxxdeps(VERBOSE, root_path, bzl, INCLUDE_DIRS, src_main, src_test_main):
    try:
        with open(root_path+'/cxxdeps.txt', 'r') as fd:
            x=fd.readlines()
            print("cxxbuild: get_bazelfiles_from_cxxdeps")
            #print(x)
            # cmakelists.append("# begin dependencies from cxxdeps.txt")
            for l in x:
                if (len(l) >= 1) and (l[0] != '#') and (l[0] != '!'):
                    # good line!
                    if VERBOSE:
                        print(l)
                    fields = l.split()
                    if VERBOSE:
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
                    print("cxxdeps bazel PROJECT:", project_name, " TRIPLET:", triplet, "SYSTEM:", my_system)
                    #
                    # cmakelists.append("# cxxdeps dependency "+project_name)
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
                    if pkg_manager[0:5] == 'cmake+':
                        print("WARNING: ignoring 'cmake+' entry for BAZEL: "+project_name)
                        continue
                    if pkg_manager == 'system':
                        # AT THIS POINT, SYSTEM LIBRARY MUST HAVE ITS LIB INSIDE, example: ['m']
                        # cmakelists.append('# system dependency: -l'+project_name)
                        add_system_triplet_bazel(bzl, triplet, not_triplet, my_system, project_name)
                        # ADD TO all, test, etc... no difference!
                        continue
                    #end-if system
                    if pkg_manager == 'git' or pkg_manager == 'bazel+git':
                        git_url = fields[k]
                        k=k+1
                        git_commit = ""
                        if k < len(fields):
                            git_commit = fields[k]
                            k=k+1
                        if git_commit == "":
                            print("ERROR: bazel+git requires Commit field!")
                            assert(False)
                        # attach it to bazel dev_dependency, if mode is 'test'
                        if mode == 'test':
                            bzl.MODULE.append("bazel_dep(name = \""+project_name+"\", dev_dependency=True)")
                            for test_target in bzl.targets_tests:
                                for l in libs:
                                    test_target[-1] = test_target[-1] + "\"@"+project_name+"//:"+l+"\"," 
                        # attach it to libraries, binaries and test binaries, if mode is *
                        if mode == '*':
                            bzl.MODULE.append("bazel_dep(name = \""+project_name+"\")")
                            for inc_target in bzl.targets_include:
                                for l in libs:
                                    inc_target[-1] = inc_target[-1] + "\"@"+project_name+"//:"+l+"\"," 
                            for main_target in bzl.targets_main:
                                for l in libs:
                                    main_target[-1] = main_target[-1] + "\"@"+project_name+"//:"+l+"\","  
                            for test_target in bzl.targets_tests:
                                for l in libs:
                                    test_target[-1] = test_target[-1] + "\"@"+project_name+"//:"+l+"\"," 
                        # for all modes now!
                        bzl.MODULE.append("git_override(")
                        bzl.MODULE.append("    module_name = \""+project_name+"\",")
                        bzl.MODULE.append("    remote = \""+git_url+"\",")
                        bzl.MODULE.append("    commit = \""+git_commit+"\",")
                        bzl.MODULE.append(")")
                        continue
                    if pkg_manager == 'bcr' or pkg_manager == 'bazel+bcr':
                        # attach it to bazel dev_dependency, if mode is 'test'
                        if mode == 'test':
                            bzl.MODULE.append("bazel_dep(name = \""+project_name+"\", version = \""+version_number+"\", dev_dependency=True)")
                            for test_target in bzl.targets_tests:
                                for l in libs:
                                    test_target[-1] = test_target[-1] + "\"@"+project_name+"//:"+l+"\"," 
                        # attach it to libraries, binaries and test binaries, if mode is *
                        if mode == '*':
                            bzl.MODULE.append("bazel_dep(name = \""+project_name+"\", version = \""+version_number+"\")")
                            for inc_target in bzl.targets_include:
                                for l in libs:
                                    inc_target[-1]  = inc_target[-1]  + "\"@"+project_name+"//:"+l+"\"," 
                            for main_target in bzl.targets_main:
                                for l in libs:
                                    main_target[-1] = main_target[-1] + "\"@"+project_name+"//:"+l+"\","  
                            for test_target in bzl.targets_tests:
                                for l in libs:
                                    test_target[-1] = test_target[-1] + "\"@"+project_name+"//:"+l+"\"," 
                        continue
                # end if not comment
            # end for line
        # end cxxdeps

    except FileNotFoundError:
        if VERBOSE:
            print("cxxbuild bazel: File cxxdeps.txt does not exist... ignoring it!")

    return bzl

def get_toml_dep(VERBOSE, dep_name, section_name, dep_object):
    if VERBOSE:
        print("get_toml_dep(...) dep_name: ", dep_name, " section:", section_name, " dep_object:", dep_object)
    local_dep = []
    # check real name (or alias)
    for x1, y1 in dep_object.items():
        if x1 == "alias":
            dep_name = y1
    build=""   # build system preferred
    for x1, y1 in dep_object.items():
        if x1 == "build":
            build = y1+"+"
    triplet=""
    for x1, y1 in dep_object.items():
        if x1 == "platform":
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
                dep_type = build+x1   # some "git" type
                complement = y1 # URL
                has_tag = False
                has_commit = False
                for x2, y2 in dep_object.items():
                    if x2 == "tag":
                        version = "\""+y2+"\""
                        has_tag = True
                    if x2 == "commit":
                        complement = complement + " " + y2
                        has_commit = True
                if has_tag and has_commit:
                    print("WARNING: get_toml_dep() git has both TAG and COMMIT!")
        for x1, y1 in dep_object.items():
            if x1 == "bcr":
                dep_type = build+x1   # some "git" type
                print("WARNING: get_toml_dep() bazel 'bcr' package must be the same as dep_name or alias!")
                assert(dep_name == y1)
                for x2, y2 in dep_object.items():
                    if x2 == "version":
                        version = "\""+y2+"\""
        # end git or bcr

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

def add_system_triplet_bazel(bzl, triplet, not_triplet, my_system, project_name):
    assert(triplet != "")
    if triplet == "windows":
        if not_triplet:
            bzl.cxxopt_linux.append("-l"+project_name)
            bzl.cxxopt_macos.append("-l"+project_name)
        else:
            bzl.cxxopt_windows.append("-l"+project_name)
    if triplet == "linux":
        if not_triplet:
            bzl.cxxopt_windows.append("-l"+project_name)
            bzl.cxxopt_macos.append("-l"+project_name)
        else:
            bzl.cxxopt_linux.append("-l"+project_name)
    if triplet == "osx":
        if not_triplet:
            bzl.cxxopt_linux.append("-l"+project_name)
            bzl.cxxopt_windows.append("-l"+project_name)
        else:
            bzl.cxxopt_linux.append("-l"+project_name)
    return True

def generate_cmakelists(VERBOSE, cppstd, cppgnu, root_path, INCLUDE_DIRS, INCLUDE_EXT, DEFINITIONS, EXTRA_SOURCES, COMPILER, STDLIB, IMPORTS, CMAKE_SET, CMAKE_UNSET, src_main, src_test_main, src_list, src_test_nomain, src_modules):
    # READ cxxdeps.txt file, if available...
    # AT THIS POINT, ASSUMING 'cmake' OPTION (NO 'bazel' FOR NOW!)
    cmakelists = []
    cmakelists.append("cmake_minimum_required(VERSION 4.0)")
    if (COMPILER != ""):
        cmakelists.append("set (CMAKE_CXX_COMPILER "+COMPILER+")")
    if (STDLIB != ""):
        cmakelists.append("set(CMAKE_CXX_FLAGS \"${CMAKE_CXX_FLAGS} -stdlib="+STDLIB+"\")")
    if ("std" in IMPORTS):
        cmakelists.append("set(CMAKE_EXPERIMENTAL_CXX_IMPORT_STD \"a9e1cf81-9932-4810-974b-6eccaf14e457\")")
        cmakelists.append("set(CMAKE_CXX_MODULE_STD 1)")
    cmakelists.append("project(my-project LANGUAGES CXX VERSION 0.0.1)")
    cmakelists.append("set (CMAKE_CXX_STANDARD "+cppstd+")") 
    cmakelists.append("set (CMAKE_CXX_STANDARD_REQUIRED ON)")
    if cppgnu:
        cmakelists.append("set (CMAKE_CXX_EXTENSIONS ON)")
    else:
        cmakelists.append("set (CMAKE_CXX_EXTENSIONS OFF)")
    cmakelists.append("set (CMAKE_EXPORT_COMPILE_COMMANDS ON)")
    cmakelists.append("Include(FetchContent)")
    for c in CMAKE_SET:
        # TODO: check set type! type1: JUST_NAME   type2: DEF="value", only ON and OFF now
        cmakelists.append("set("+c+" ON)")
    for c in CMAKE_UNSET:
        cmakelists.append("set("+c+" OFF)")
    # add definitions!
    for d in DEFINITIONS:
        # TODO: check definition type! type1: JUST_DEF   type2: DEF="value"
        cmakelists.append("add_definitions(-D"+d+")")
    #
    cmakelists.append("# add all executables")
    COUNT_APP_ID=1
    all_apps = []
    # add_library for module libraries (.cppm)
    cxx_module_list = ""
    for filepath, app_name in src_modules.items():
        cmakelists.append("add_library("+app_name[1]+" )   # cxx module: "+app_name[1])
        cmakelists.append("target_sources("+app_name[1]+" PUBLIC  FILE_SET CXX_MODULES FILES "+filepath.replace("\\", "/")+")")
        cxx_module_list = cxx_module_list + " " + app_name[1]
    # add_executable for binaries
    for filepath, app_name in src_main.items():
        cmakelists.append("add_executable("+app_name[1]+" "+filepath.replace("\\", "/")+" )    # main")
        if cxx_module_list != "":
            cmakelists.append("target_link_libraries("+app_name[1]+" "+cxx_module_list+" )")    

    # add_executable for test binaries
    print("cxxbuild cmake: finding test executables!")
    # if no main is found, then each test is assumed to be independent!
    if len(src_test_main.items()) == 0:
        print("WARNING: no main() is found for tests... using main-less strategy!")
        src_test_main = src_test_nomain
    for filepath, app_name in src_test_main.items():
        cmakelists.append("add_executable("+app_name[1]+" "+filepath.replace("\\", "/")+" )")
        if cxx_module_list != "":
            cmakelists.append("target_link_libraries("+app_name[1]+" PRIVATE "+cxx_module_list+" )")


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
    generate_txt_from_toml(VERBOSE, root_path)

    # cxxdeps.txt
    cmakelists = get_cmakelists_from_cxxdeps(VERBOSE, root_path, cmakelists, INCLUDE_DIRS, src_main, src_test_main)

    # ======== begin add sources ========
    cmakelists.append("# finally, add all sources")
    cmakelists.append("set(SOURCES")
    # add extra sources!
    for esrc in EXTRA_SOURCES:
        cmakelists.append("\t"+esrc)
    # get all sources not in main() list (no duplicates exist)
    clean_list = []
    clean_list_main = []
    for f in src_list:
        clean_list.append(f.replace("\\", "/"))
    #clean_list = list(set(clean_list)) # do not do this!
    for filepath, app_name in src_main.items():
        clean_list_main.append(filepath.replace("\\", "/"))
    #clean_list_main = list(set(clean_list_main))  # do not do this!
    clean_list = [x for x in clean_list if x not in clean_list_main]
    for f in clean_list:
        cmakelists.append("\t"+f)
    cmakelists.append(")")
    # ======== end add sources ========
    for filepath, app_name in src_main.items():
        cmakelists.append("target_sources("+app_name[1]+" PRIVATE ${SOURCES})")
    for filepath, app_name in src_test_main.items():
        cmakelists.append("target_sources("+app_name[1]+" PRIVATE ${SOURCES})")


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

def generate_bazelfiles(VERBOSE, cppstd, root_path, INCLUDE_DIRS, INCLUDE_EXT, DEFINITIONS, EXTRA_SOURCES, src_main, src_test_main, src_list, src_test_nomain):
    # READ cxxdeps.txt file, if available...
    # AT THIS POINT, ASSUMING 'cmake' OPTION (NO 'bazel' FOR NOW!)
    bzl = BazelFiles()
    bzl.MODULE = []
    bzl.MODULE.append("bazel_dep(name = \"hedron_compile_commands\", dev_dependency = True)")
    bzl.MODULE.append("git_override(")
    bzl.MODULE.append("    module_name = \"hedron_compile_commands\",")
    bzl.MODULE.append("    remote = \"https://github.com/hedronvision/bazel-compile-commands-extractor.git\",")
    bzl.MODULE.append("    commit = \"daae6f40adfa5fdb7c89684cbe4d88b691c63b2d\",")
    bzl.MODULE.append(")")
    bzl.MODULE.append("# bazel run @hedron_compile_commands//:refresh_all")
    bzl.MODULE.append("#")

    bzl.bazelrc = []
    bzl.bazelrc.append("common --enable_platform_specific_config")
    bzl.bazelrc.append("#")

    bzl.BUILD_root = []
    bzl.BUILD_root.append("# load(\"@rules_cc//cc:defs.bzl\", \"cc_binary\", \"cc_library\")")
    bzl.BUILD_root.append("#")
    bzl.BUILD_root.append("package(")
    bzl.BUILD_root.append("    default_visibility = [\"//visibility:public\"],")
    bzl.BUILD_root.append(")")
    bzl.BUILD_root.append("#")

    bzl.BUILD_tests = []
    #bzl.BUILD_tests.append("load(\"@rules_cc//cc:defs.bzl\", \"cc_library\", \"cc_test\")")
    #bzl.BUILD_tests.append("package(default_visibility = [\"//visibility:public\"])")
    bzl.BUILD_tests.append("\n#")
    bzl.BUILD_tests.append("test_suite(")
    bzl.BUILD_tests.append("    name = \"suite-tests\",")
    bzl.BUILD_tests.append("    tests = [")
    bzl.BUILD_tests.append("        \"all_tests\"")
    bzl.BUILD_tests.append("    ]")
    bzl.BUILD_tests.append(")\n")

    # add sources! ADD LATER IN GLOBs
    nomain_src_list = []
    for f in src_list:
        for filepath, app_name in src_main.items():
            filepath2 = filepath.replace("\\", "/")
            f2 = f.replace("\\", "/")
            if filepath2 != f2:
                nomain_src_list.append(f2)
    #
    bzl.targets_main = []
    bzl.targets_tests = []
    bzl.targets_include = []

    # add_executable for binaries
    for filepath, app_name in src_main.items():
        target_main = []
        target_main.append("\ncc_binary(")
        target_main.append("    name = \""+app_name[1]+"\",")
        target_main.append("    srcs = glob([")
        target_main.append("\t\t\""+filepath.replace("\\", "/")+"\",")
        for k in nomain_src_list:
            target_main.append("\t\t\""+k+"\",")
        target_main.append("\t\t\""+"src/*.h\"") # TODO: fix 'src'
        target_main.append("\t]),")
        bzl.targets_main.append(target_main)
    #

    # add_executable for test binaries
    print("cxxbuild: generate_bazelfiles() finding test executables!")
    # if no main is found, then each test is assumed to be independent!
    if len(src_test_main.items()) == 0:
        print("WARNING: no main() is found for tests... using main-less strategy!")
        src_test_main = src_test_nomain
    for filepath, app_name in src_test_main.items():
        target_tests = []
        target_tests.append("\ncc_test(")
        target_tests.append("    name = \"all_tests\",")
        target_tests.append("    srcs = glob([")
        target_tests.append("\t\t\""+filepath.replace("\\", "/")+"\",")
        target_tests.append("    ]),")
        bzl.targets_tests.append(target_tests)

    # INCLUDE_DIRS will act as header-only libraries
    #  => DO NOT ADD SOURCE FILES INTO include FOLDERS!!!
    if VERBOSE:
        print("generate_bazelfiles() INCLUDE_DIRS:", INCLUDE_DIRS)
    # FOR NOW: make sure at most a single include exists, for bazel sake!
    assert(len(INCLUDE_DIRS) <= 1) 
    for i in range(len(INCLUDE_DIRS)):
        incdir = INCLUDE_DIRS[i]
        target_include = []
        target_include.append("\ncc_library(")
        target_include.append("    name = \"my_headers"+str(i)+"\",")
        # TODO: cannot add non-existing glob extensions anymore on bazel!
        # target_include.append("    hdrs = glob([\""+incdir+"/**/*.hpp\",\""+incdir+"/**/*.h\"]),")
        hdrs_str = "    hdrs = "
        if len(INCLUDE_EXT)==0:
            hdrs_str = hdrs_str + "[],"
        else:
            hdrs_str = hdrs_str + "glob(["
            first = True
            for inc_ext in INCLUDE_EXT:
                if not first:
                    hdrs_str = hdrs_str + ","
                first = False
                hdrs_str = hdrs_str + "\""+incdir+"/**/*" + inc_ext + "\""
            hdrs_str = hdrs_str + "]),"
        target_include.append(hdrs_str)
        target_include.append("    includes = [\""+incdir+"\"],")
        target_include.append("    # no 'dep' attribute in cc_library")
        target_include.append("    # dep = [")
        bzl.targets_include.append(target_include)
        for tmain in bzl.targets_main:
            tmain.append("\tdeps = [\":my_headers"+str(i)+"\",")
        for ttest in bzl.targets_tests:
            ttest.append("\tdeps = [\"//:my_headers"+str(i)+"\",")
    if len(INCLUDE_DIRS) == 0:
        for tmain in bzl.targets_main:
            tmain.append("\tdeps = [")
        for ttest in bzl.targets_tests:
            ttest.append("\tdeps = [")

    # finish basic part, begin dependencies
    if VERBOSE:
        print("bzl.targets_main:    COUNT =", len(bzl.targets_main))
        print("bzl.targets_tests:   COUNT =", len(bzl.targets_tests))
        print("bzl.targets_include: COUNT =", len(bzl.targets_include))
    #
    generate_txt_from_toml(VERBOSE, root_path)

    # cxxdeps.txt
    bzl = get_bazelfiles_from_cxxdeps(VERBOSE, root_path, bzl, INCLUDE_DIRS, src_main, src_test_main)

    # finalize all files

    for tmain in bzl.targets_main:
        tmain[-1] = tmain[-1] + "]\n)"
    for ttest in bzl.targets_tests:
        ttest[-1] = ttest[-1] + "]\n)"
    for tinc in bzl.targets_include:
        tinc[-1]  = tinc[-1]  + "]\n)"

    # TODO: check if files exist and update... now, just overwrite!

    # ============ create MODULE.bazel ===========
    with open(root_path+'/MODULE.bazel', 'w') as file:
        file.write('\n'.join(bzl.MODULE))

    print("-----------------------------------")
    print("MODULE.bazel generated on folder:")
    print(" => "+root_path+'/MODULE.bazel')
    print("-----------------------------------")

    # ============ create BUILD.bazel ===========
    with open(root_path+'/BUILD.bazel', 'w') as file:
        file.write('\n'.join(bzl.BUILD_root))
        for tmain in bzl.targets_main:
            file.write('\n'.join(tmain))
        for tinclude in bzl.targets_include:
            file.write('\n'.join(tinclude))
        if len(bzl.targets_tests) > 0:
            # tests part!
            file.write('\n'.join(bzl.BUILD_tests))
            for ttest in bzl.targets_tests:
                file.write('\n'.join(ttest))


    print("-----------------------------------")
    print("BUILD.bazel generated on folder:")
    print(" => "+root_path+'/BUILD.bazel')
    print("-----------------------------------")

    # ============ create .bazelrc ===========
    lwin = "build:windows --cxxopt=-std:c++"+cppstd
    for topt in bzl.cxxopt_windows:
        lwin += " --cxxopt="+topt
    llinux = "build:linux --cxxopt=-std=c++"+cppstd
    for topt in bzl.cxxopt_windows:
        llinux += " --cxxopt="+topt
    lmacos = "build:macos --cxxopt=-std=c++"+cppstd
    for topt in bzl.cxxopt_windows:
        lmacos += " --cxxopt="+topt
    bzl.bazelrc.append(lwin)
    bzl.bazelrc.append(llinux)
    bzl.bazelrc.append(lmacos)

    with open(root_path+'/.bazelrc', 'w') as file:
        file.write('\n'.join(bzl.bazelrc))

    print("-----------------------------------")
    print(".bazelrc generated on folder:")
    print(" => "+root_path+'/.bazelrc')
    print("-----------------------------------")

    # ============ create tests/BUILD ===========
    # TODO: fix 'tests'
    #with open(root_path+'/tests/BUILD', 'w') as file:
    #    file.write('\n'.join(bzl.BUILD_tests))
    #    for ttest in bzl.targets_tests:
    #        file.write('\n'.join(ttest))

    #print("-----------------------------------")
    #print("tests/BUILD generated on folder:")
    #print(" => "+root_path+'/tests/BUILD')
    #print("-----------------------------------")

    # ============ create .bazelignore ===========
    with open(root_path+'/.bazelignore', 'w') as file:
        file.write('build/\n')

    print("-----------------------------------")
    print(".bazelignore generated on folder:")
    print(" => "+root_path+'/.bazelignore')
    print("-----------------------------------")

    print("FINISHED BAZEL GENERATION!")

def generate_txt_from_toml(VERBOSE, root_path):
    try:
        cxxdeps_all = []
        cxxdeps_test = []
        cxxdeps_dev = []
        with open(root_path+'/cxxdeps.toml', 'r') as toml_file:
            print("Loading cxxdeps.toml file...")
            import toml
            data = toml.load(toml_file)
            #
            for section_name, section_data in data.items():
                if VERBOSE:
                    print(f"SECTION=[{section_name}]")
                # Iterate over dependencies within each section
                for dependency_name, dependency_info in section_data.items():
                    if VERBOSE:
                        print("processing dependency: ", dependency_name)
                    if isinstance(dependency_info, list):
                        for d in dependency_info:
                            x = get_toml_dep(VERBOSE, dependency_name, section_name, d)
                            if section_name == "test":
                                cxxdeps_test.append(x)
                            elif section_name == "dev":
                                cxxdeps_dev.append(x)
                            else:
                                cxxdeps_all.append(x)
                    elif isinstance(dependency_info, dict):
                        x = get_toml_dep(VERBOSE, dependency_name, section_name, dependency_info)
                        if section_name == "test":
                            cxxdeps_test.append(x)
                        elif section_name == "dev":
                            cxxdeps_dev.append(x)
                        else:
                            cxxdeps_all.append(x)
                    else:
                        print("Dependency info is neither a list nor an object.")
                        assert(False)
                if VERBOSE:
                    print("\n")
        # end with
        # finishing .toml file
        if VERBOSE:
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
        if VERBOSE:
            print("cxxdeps: File cxxdeps.toml does not exist... ignoring it!")

def check_cmake():
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

def run_cmake(VERBOSE, root_path):
    # ============ build with cmake+ninja ===========
    # check_cmake() # already checked!
    #
    # STEP 1.5: debug only
    if VERBOSE:
        CMAKE_CMD="cat "+root_path+"/CMakeLists.txt"
        print("showing CMakeLists.txt... "+CMAKE_CMD)
        x=subprocess.call(list(filter(None, CMAKE_CMD.split(' '))))
        print('cat result:', x)
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

def check_bazel():
    # STEP 1: check that 'bazel' command exists
    CHECK_BAZEL_CMD="bazel --version"
    print("Please install latest bazel with NVM: bash -i -c \"npm install -g @bazel/bazelisk\"")
    print("   - on windows: choco install bazel")
    print("   - on macos:   brew install bazelisk")
    print("or visit bazel website: https://bazel.build/install")
    print("checking bazel command now...")
    x=subprocess.call(list(filter(None, CHECK_BAZEL_CMD.split(' '))))
    print('check result:', x)
    assert(x == 0)

def run_bazel(VERBOSE, root_path):
    # ============ build with bazel ===========
    # check_bazel() # already checked!
    #
    # STEP 1.5: debug only
    if VERBOSE:
        BAZEL_CMD="cat "+root_path+"/MODULE.bazel"
        print("showing MODULE.bazel... "+BAZEL_CMD)
        x=subprocess.call(list(filter(None, BAZEL_CMD.split(' '))))
        print('\nbazel result:', x)
        assert(x == 0)
    #
    if VERBOSE:
        BAZEL_CMD="cat "+root_path+"/BUILD.bazel"
        print("showing BUILD.bazel... "+BAZEL_CMD)
        x=subprocess.call(list(filter(None, BAZEL_CMD.split(' '))))
        print('\nbazel result:', x)
        assert(x == 0)
    #
    # STEP 2: build with bazel
    BAZEL_CMD="bazel build ..."
    print("building...\n"+BAZEL_CMD)
    x=subprocess.call(list(filter(None, BAZEL_CMD.split(' '))), cwd=root_path)
    print('bazel result:', x)
    assert(x == 0)


# detect if it's 'cmd' for windows, but not 'bash'
def is_cmd():
    return os.name == 'nt' and 'WSL_DISTRO_NAME' not in os.environ


def main():
    print("======================================")
    print("     welcome to cxxdeps/cxxbuild      ")
    print("======================================")
    print(version())
    # options: 'posix' or 'nt'
    print("os: "+os.name+"; platform: "+platform.system())
    # options: 'Darwin', 'Windows' or 'Linux'
    if platform.system() == "Linux":
        print("linux: "+platform.freedesktop_os_release().get("VERSION_CODENAME"))
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
        # when in 'build' mode, must take path explicitly from third argument!
        # example: cxxbuild build .
        if len(sys.argv) > 2:
            root_path = sys.argv[2]
        else:
            usage()
            exit()  

    verbose=False
    
    build_options_args = []
    for i in range(len(sys.argv)):
        if (sys.argv[i] == "--src"):
            build_options_args.append("!src \""+str(sys.argv[i + 1])+"\"")
        if (sys.argv[i] == "--extrasrc"):
            build_options_args.append("!extrasrc "+str(sys.argv[i + 1]))
        if (sys.argv[i] == "--tests"):
            build_options_args.append("!tests \""+str(sys.argv[i + 1])+"\"")
        if (sys.argv[i] == "--include"):
            build_options_args.append("!include \""+str(sys.argv[i + 1])+"\"")
        if (sys.argv[i] == "--ignore"):
            build_options_args.append("!ignore "+str(sys.argv[i + 1]))
        if (sys.argv[i] == "--define"):
            build_options_args.append("!define "+str(sys.argv[i + 1]))
        if (sys.argv[i] == "--cmake-set"):
            build_options_args.append("!cmake-set "+str(sys.argv[i + 1]))
        if (sys.argv[i] == "--cmake-unset"):
            build_options_args.append("!cmake-unset "+str(sys.argv[i + 1]))
            # --keep ??? do not re-regenerate CMakeLists... only build! WARN if differences found? DIFF?s
        if (sys.argv[i] == "--compiler"):
            build_options_args.append("!compiler \""+str(sys.argv[i + 1])+"\"")
        if (sys.argv[i] == "--stdlib"):
            build_options_args.append("!stdlib "+str(sys.argv[i + 1]))
        if (sys.argv[i] == "--import"):
            build_options_args.append("!import "+str(sys.argv[i + 1]))
        if (sys.argv[i] == "--verbose"):
            build_options_args.append("!verbose")
            verbose=True  # needed to advance this special option!
            print("cxxbuild VERBOSE mode is enabled: ", verbose)
        if (sys.argv[i] == "--cmake"):
            build_options_args.append("!build cmake")
        if (sys.argv[i] == "--bazel"):
            build_options_args.append("!build bazel")
        if (sys.argv[i] == "--c++11"):
            build_options_args.append("!std c++11")
        if (sys.argv[i] == "--c++14"):
            build_options_args.append("!std c++14")
        if (sys.argv[i] == "--c++17"):
            build_options_args.append("!std c++17")
        if (sys.argv[i] == "--c++20"):
            build_options_args.append("!std c++20")
        if (sys.argv[i] == "--c++23"):
            build_options_args.append("!std c++23")
        if (sys.argv[i] == "--gnu++23"):
            build_options_args.append("!std gnu++23")
        if (sys.argv[i] == "--c++26"):
            build_options_args.append("!std c++26")

    if verbose:
        print("build options from args: "+str(build_options_args))
    #
    build_options = []
    # TODO: convert .toml to .txt here, if necessary!
    # get more build options for cxxdeps.txt
    try:
        with open(root_path+'/cxxdeps.txt', 'r') as fd:
            x=fd.readlines()
            for l in x:
                if (len(l) >= 1) and (l[0] == '!'):
                    build_options.append(l)
    except FileNotFoundError:
        if verbose:
            print("File cxxdeps.txt does not exist... ignoring it!")
    
    # merge with argument build options (priority/override is LAST)
    for op in build_options_args:
        build_options.append(op)

    if verbose:
        print("build options (including cxxdeps): "+str(build_options))

    # begin processing build options
    search_src="src"
    search_tests="tests"
    search_include="include"
    #
    use_cmake=None
    use_bazel=None
    cppstd="17"
    cppgnu=False      # disable extensions by default
    COMPILER = ""     # cxx compiler path
    STDLIB = ""       # libc++ ? useful for clang on linux...
    INCLUDE_DIRS = []
    DEFINITIONS = []
    EXTRA_SOURCES = []
    IMPORTS = []
    CMAKE_SET = []
    CMAKE_UNSET = []
    IGNORE = []
    # ignore build/ folder by default
    IGNORE.append("build/")
    for op in build_options:
        # import shlex
        # oplist = shlex.split(op)
        oplist = op.split()
        if verbose:
            print(op.split())
        if oplist[0] == '!version':
            MIN_CXXBUILD_VERSION=oplist[1]
            current_version = version().split("=")[1]
            # from setuptools._distutils.version import LooseVersion, StrictVersion
            # if LooseVersion(current_version) < LooseVersion(MIN_CXXBUILD_VERSION):
            from packaging.version import Version
            if Version(current_version) < Version(MIN_CXXBUILD_VERSION):
                print("Insufficient CXXBUILD version! Please upgrade!")
                print("Current version: "+current_version)
                print("Required version (cxxdeps): "+MIN_CXXBUILD_VERSION)
                print("Aborting...")
                exit(1)
        if oplist[0] == '!include':
            INCLUDE_DIRS.append(oplist[1].strip("\""))
        if oplist[0] == '!ignore':
            IGNORE.append(op[len(oplist[0]):].strip())
        if oplist[0] == '!define':
            DEFINITIONS.append(op[len(oplist[0]):].strip())
        if oplist[0] == '!extrasrc':
            EXTRA_SOURCES.append(op[len(oplist[0]):].strip())
        if oplist[0] == '!src':
            search_src = oplist[1].strip("\"")
        if oplist[0] == '!tests':
            search_tests = oplist[1].strip("\"")
        if oplist[0] == '!compiler':
            COMPILER = oplist[1].strip("\"")
        if oplist[0] == '!stdlib':
            STDLIB = op[len(oplist[0]):].strip()
        if oplist[0] == '!import':
            module_name = op[len(oplist[0]):].strip()
            if module_name != "std":
                print("cxxbuild error: can only import module 'std', not '",module_name,"'")
                exit(1)
            IMPORTS.append(module_name)
        if oplist[0] == '!cmake-set':
            CMAKE_SET.append(op[len(oplist[0]):].strip())
        if oplist[0] == '!cmake-unset':
            CMAKE_UNSET.append(op[len(oplist[0]):].strip())
        if oplist[0] == '!verbose':
            verbose = True
        if oplist[0] == '!build' and oplist[1] == 'cmake':
            if use_bazel == True:
                print("cxxbuild error: cannot redefine build system 'bazel' to 'cmake'")
                exit(1)
            use_cmake = True
            use_bazel = False
        if oplist[0] == '!build' and oplist[1] == 'bazel':
            if use_cmake == True:
                print("cxxbuild error: cannot redefine build system 'cmake' to 'bazel'")
                exit(1)
            use_cmake = False
            use_bazel = True
        if oplist[0] == '!std' and oplist[1] == 'c++11':
            cppstd="11"
        if oplist[0] == '!std' and oplist[1] == 'c++14':
            cppstd="14"
        if oplist[0] == '!std' and oplist[1] == 'c++17':
            cppstd="17"
        if oplist[0] == '!std' and oplist[1] == 'c++20':
            cppstd="20"
        if oplist[0] == '!std' and oplist[1] == 'c++23':
            cppstd="23"
        if oplist[0] == '!std' and oplist[1] == 'gnu++23':
            cppstd="23"
            cppgnu=True
        if oplist[0] == '!std' and oplist[1] == 'c++26':
            cppstd="26"
        
    # build system defaults to cmake
    if use_cmake is None:
        use_cmake = True
        use_bazel = False

    #
    return run_build(verbose, root_path, use_cmake, use_bazel, cppstd, cppgnu, search_src, search_tests, search_include, INCLUDE_DIRS, DEFINITIONS, EXTRA_SOURCES, IGNORE, COMPILER, STDLIB, IMPORTS, CMAKE_SET, CMAKE_UNSET)

def run_build(VERBOSE, root_path, use_cmake, use_bazel, cppstd, cppgnu, search_src, search_tests, search_include, INCLUDE_DIRS, DEFINITIONS, EXTRA_SOURCES, IGNORE, COMPILER, STDLIB, IMPORTS, CMAKE_SET, CMAKE_UNSET):
    #
    #if VERBOSE:
    print("cxxbuild: begin build on root_path =",root_path)
    # ===================================
    # test is cmake or bazel is available
    # ===================================
    if use_cmake:
        print("BUILD WITH CMAKE! Checking...")
        check_cmake()
    elif use_bazel:
        print("BUILD WITH BAZEL! Checking...")
        check_bazel()
    else:
        print("BUILD ERROR! NOT CMAKE OR BAZEL")
        assert(False)
    print("Check passed!\n")

    # find all source files,
    # find all files with an entry point,
    src_list = []
    src_modules = {}
    src_main = {}
    # ENFORCING THIS PATH... MUST ADD MULTIPLE PATH OPTION!
    # src_paths = [root_path, root_path+"/src"] 
    src_paths = [root_path+"/"+search_src] 
    if VERBOSE:
        print("src_paths=", src_paths)
    entrypoint = "main("  # Pattern to find main(), or main(int argc, ...), etc
    #
    src_ext = ['.c', '.cc', '.cpp', '.cxx', '.c++']
    src_module_ext = ['.cppm']
    if VERBOSE:
        print('src_ext:', src_ext)
    print("cxxbuild: loading source files...")
    for src_path in src_paths:
        for root, subdirs, files in os.walk(src_path):
            root = root.removeprefix(root_path).removeprefix("/")
            if VERBOSE:
                print("checking root_SRC: ", root)
                print("checking subdirs_SRC: ", subdirs)
                print("checking files_SRC: ", files)
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
                        if VERBOSE:
                            print("checking entrypoint:", entrypoint)
                        all_lines=fd.readlines()
                        for l in all_lines:
                            # avoid commented lines (small improvement)
                            l2 = l.strip()
                            if entrypoint in l2 and l2[0] != "/" and l2[1] != "/":
                                src_main[file_path] = (root, file_name)
                if ext in src_module_ext:
                    file_path = os.path.join(root, file)
                    src_modules[file_path] = (root, file_name)
        # end-for src_path
    # end-for src_paths

    if VERBOSE:
        print("src_main:", src_main)
        print("src_list:", src_list)
        print("src_modules:", src_modules)

    # finding tests...

    src_test_list = []
    src_test_main = {}
    src_test_nomain = {}
    #
    if VERBOSE:
        print(src_ext)
    print("cxxbuild: loading source test files...")
    for root, subdirs, files in os.walk(root_path+"/"+search_tests):
        root = root.removeprefix(root_path).removeprefix("/")
        if VERBOSE:
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
                    if VERBOSE:
                        print("checking entrypoint:", entrypoint)
                    if entrypoint in fd.read():
                        src_test_main[file_path] = (root, file_name+"_test")

    if VERBOSE:
        print("src_test_main:", src_test_main)
        print("src_test_nomain:", src_test_nomain)
        print("src_test_list:", src_test_list)

    # ---------------------------------
    # FIX app names (avoid duplicates!)
    COUNT_APP_ID=1
    all_apps = []
    for filepath, app_name in src_main.items():
        app_name_list = list(app_name)
        app_name1 = app_name_list[1]
        while app_name1 in all_apps:
            COUNT_APP_ID = COUNT_APP_ID + 1
            app_name1 = app_name_list[1] + str(COUNT_APP_ID) # concat number
        all_apps.append(app_name1)
        app_name_list[1] = app_name1
        src_main[filepath] = tuple(app_name_list) 
    # ---------------------------------

    if VERBOSE:
        print("fixed src_main: ", src_main)
    
    # SO... TIME TO FIND INCLUDE FOLDERS
    print("cxxbuild: loading include folders...")
    for root, subdirs, files in os.walk(root_path):
        root = root.removeprefix(root_path).removeprefix("/")
        #print("root: ", root)
        #print("subdirs: ", subdirs)
        #print("files: ", files)
        if "include" in subdirs:
            incdir = root+"/"+search_include
            incdir = incdir.removeprefix(root_path).removeprefix("/")
            must_ignore=False
            for ign in IGNORE:
                # ignore 'build' stuff and others in IGNORE
                if incdir.startswith(ign):
                    #if VERBOSE:  # Warning?
                    print("WARNING: '"+ign+"' prefixed folder ignored: ", incdir)
                    must_ignore=True
                    break
            if not must_ignore:
                INCLUDE_DIRS.append(incdir)
            # end-for
        # TODO: search in other places too... maybe inside src?
    # keep unique only!
    INCLUDE_DIRS = list(set(INCLUDE_DIRS))

    if VERBOSE:
        print("INCLUDE_DIRS=",INCLUDE_DIRS)
    allowed_inc_ext = [".hpp", ".h"]
    INCLUDE_EXT = []
    for inc in INCLUDE_DIRS:
        for root, subdirs, files in os.walk(root_path+"/"+inc):
            root = root.removeprefix(root_path).removeprefix("/")
            #print("INC root: ", root)
            #print("INC subdirs: ", subdirs)
            #print("INC files: ", files)
            for file in files:
                file_name, ext = os.path.splitext(file)
                if ext in allowed_inc_ext:
                    if ext in INCLUDE_EXT:
                        pass
                    else:
                        INCLUDE_EXT.append(ext)
    # for inc
    if VERBOSE:
        print("INCLUDE_EXT=",INCLUDE_EXT)

    if use_cmake == True:
        generate_cmakelists(VERBOSE, cppstd, cppgnu, root_path, INCLUDE_DIRS, INCLUDE_EXT, DEFINITIONS, EXTRA_SOURCES, COMPILER, STDLIB, IMPORTS, CMAKE_SET, CMAKE_UNSET, src_main, src_test_main, src_list, src_test_nomain, src_modules)
    elif use_bazel == True:
        generate_bazelfiles(VERBOSE, cppstd, root_path, INCLUDE_DIRS, INCLUDE_EXT, DEFINITIONS, EXTRA_SOURCES, src_main, src_test_main, src_list, src_test_nomain)
    else:
        assert(False)

    if use_cmake == True:
        run_cmake(VERBOSE, root_path)
    elif use_bazel == True:
        run_bazel(VERBOSE, root_path)
    else:
        print("UNKNOWN BUILDER! cxxbuild ERROR...")
        assert(False)

    if len(src_main.items()) > 0:
        print("OK: at least one main() has been found!")
    else:
        print("WARNING: no main() has been found!")

if __name__ == '__main__':
    main()