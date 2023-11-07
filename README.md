# cxxbuild
cxxbuild is a python script to easily build C++ programs: just invoke 'cxxbuild' and it works!

We know it is very hard to start a C++ project and learn basics of build systems such as CMake and Bazel, and package managers like conan and vcpkg... so just type "cxxbuild" and be happy!

The strongest point of this project is the `cxxdeps.txt` format, 
that allow easy specification of dependencies from different package managers.

To use it locally, just copy [cxxbuild.py](cxxbuild.py) file to your project and execute it: `python3 cxxbuild.py`

## Basic commands

`cxxbuild` has three modes:

- build mode (default): just pass some root directory with files
- clean mode (unimplemented): will clean specific build files
- lint mode (unimplemented): will lint project files
- test mode (unimplemented): will run project tests

## Running demo

`python3 cxxbuild.py demo/project1`

It will:

- read dependencies from cxxdeps.txt file (if exists)
- generate a CMakeLists.txt on project
- build with cmake+ninja (default) or any other provided build system

Generated binaries will be on `demo/project1/build/`

- `demo1`: binary with entrypoint (main) for demo (file: `src/demo1.cpp`)
- `my_test`: binary with unit tests (file: `tests/my_test.cpp`)

To clean it (since `clean` command is still unimplemented), just delete `build/` folder.

### Expected project organization

The tool cxxbuild assumes that:

- source code (.cpp, .cc, .c, etc) is located on a `src/` folder
- test code is located on a `tests/` folder
- header only libraries are located on a `include/` folder

The reason for `src/` folder is:

1. enforces some "basic" project organization (I know many people don't like a `src/` folder...)
2. recursively searching on local folder yields some issues,
as `build/` folder becomes contaminated with .cpp dependencies, so some exclusion algorithm would be necessary

The reason for `tests/` folder is:

1. enforces some "basic" project organization (I know many people don't like a `tests/` folder...)
2. it is hard to distinguish between binary `.cpp` files and unit test files, 
unless  some other "standard" is imposed, such as naming `tests.cpp` (but what about multiple tests then?)

The reason for `include/` folder is:

1. this is classic organization, c'mon!!!
2. this is necessary to isolate header only library and make it easier for other to include them... if you don't want to offer a header only library, ok then, just put everything on `src/` folder and that is fine!

These things can be easily changed, either manually on cxxbuild.py script, or by opening an issue and we discuss if some other option is really necessary... 
Note that this project does not aims to have many personalizations and complications, let's use KISS method!

## Advantages and Drawbacks

Greatest advantage of this project is to easily describe dependencies on a `cxxdeps.txt` file.

An example is:

```
fmt == "9.1.0"     [ fmt ]                    git *    https://github.com/fmtlib/fmt.git
Catch2 == "v3.3.1" [ Catch2::Catch2WithMain ] git test https://github.com/catchorg/Catch2.git
m
```

This is quite simple and powerful, with few lines describing the following:

- take `fmt` project from git repository in specific version
- take `Catch2` project from git repository in specific version and use it for tests only
- take system `-lm` dependency

The `git` part could be any package manager, such as conan and vcpkg, although not implemented yet!

- In fact, this was the most motivating part of this project, so feel free to check more painful experiences directly on [manydeps-gmp](https://github.com/manydeps/manydeps-gmp) project!

Hopefully, when this project is finished, C++ will be a better place for all of us :)

## Related Works

- See ccbuild from debian
- See mantle project (experimental but with similar ideas)

None of them support dependencies, such as `cxxdeps.txt`, or even build systems such as cmake and bazel.

## License

MIT License

Copyleft 2023 

Igor Machado Coelho

