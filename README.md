# cxxbuild
cxxbuild is a python script to easily build C++ programs: just invoke 'cxxbuild' and it works!

We know it is very hard to start a C++ project and learn basics of build systems such as CMake and Bazel, and package managers like conan and vcpkg... so just type "cxxbuild" and be happy!

The strongest point of this project is the `cxxdeps.txt` format, 
that allow easy specification of dependencies from different package managers.

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

