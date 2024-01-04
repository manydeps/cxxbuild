# cxxbuild / cxxdeps

[![Demo on windows, linux and macos](https://github.com/manydeps/cxxbuild/actions/workflows/demo.yml/badge.svg)](https://github.com/manydeps/cxxbuild/actions/workflows/demo.yml)

![C++17](https://img.shields.io/badge/std-c%2B%2B17-blue)

[![DOI](https://zenodo.org/badge/715821683.svg)](https://zenodo.org/doi/10.5281/zenodo.10447208)

Version: `cxxbuild version=1.5.1`  Installation: `pip install cxxbuild`

cxxbuild is a python script to easily build C++ programs: just invoke 'cxxbuild' and it works!

For basic introduction, read the post: [Using cxxbuild to easily build C++ project with tests and dependencies](https://igormcoelho.medium.com/using-cxxbuild-to-easily-build-c-project-with-tests-and-dependencies-a3726b453f75)

We know it is very hard to start a C++ project and learn basics of build systems such as CMake and Bazel, and package managers like conan and vcpkg... so just type "cxxbuild" and be happy!

The strongest point of this project is the `cxxdeps.txt` format, 
that allow easy specification of dependencies from different package managers (in similar style of python `requirements.txt` format)

To use it locally, just copy [cxxbuild/cxxbuild.py](cxxbuild/cxxbuild.py) file to your project and execute it: `python3 cxxbuild.py help`

Or, just install it from pip: `pip install cxxbuild`

Then, just run: `cxxbuild help`

## Basic commands

`cxxbuild` has four main modes (three unimplemented, yet):

- build mode (default): just pass some root directory with files
- clean mode (unimplemented): will clean specific build files
- lint mode (unimplemented): will lint project files
- test mode (unimplemented): will run project tests

## Running demos 

```
python3 cxxbuild/cxxbuild.py demo/project1
python3 cxxbuild/cxxbuild.py demo/project2
python3 cxxbuild/cxxbuild.py demo/project3
```

Each of them should build some specific demo project, without any issues.

### Demo also working for Bazel (beta)

If you prefer Bazel Build, then you can try this:

```
python3 cxxbuild/cxxbuild.py demo/project1 --bazel
```

It will automatically generate files such as `MODULE.bazel` and `BUILD.bazel`.

## Test summary for demos

- demo/project1: runs on linux, osx and windows* (bash only)
- demo/project2: runs on linux, osx and windows (bash and cmd)
- demo/project3: runs on linux, osx and windows* (bash only)

(*) Some limitations on windows/cmd are related to fmt dependency on cmake, not cxxbuild.

## Running demo 1 (explained)

`python3 cxxbuild/cxxbuild.py demo/project1`

OR, after installation:

`cxxbuild demo/project1`


It will:

- read dependencies from cxxdeps.txt file, if available
- generate a CMakeLists.txt on project (backup your file if you already have one!)
- build with cmake+ninja (default) or any other provided build system

Generated binaries will be on `demo/project1/build/`

- `demo1`: binary with entrypoint (main) for demo (file: `src/demo1.cpp`)
- `my_test`: binary with unit tests (file: `tests/my_test.cpp`)

To clean it (since `clean` command is still unimplemented), just delete `build/` folder.

### Expected project organization

The tool cxxbuild assumes that:

- source code (.cpp, .cc, .c, etc) is located on a `src/` folder
    * this can be changed with `--src SRC_PATH` option
- test code is located on a `tests/` folder
    * this can be changed with `--tests TEST_PATH` option
- header only libraries are located on a `include/` folder
    * this can be changed with `--include INCLUDE_PATH` option

The reason for `src/` folder is:

1. enforces some "basic" project organization (I know many people don't like a `src/` folder...)
2. recursively searching source files on root folder yields some issues,
as `build/` folder in same directory level becomes contaminated with external .cpp dependencies, thus requiring some clever exclusion algorithm

The reason for `tests/` folder is:

1. enforces some "basic" project organization (I know many people don't like a `tests/` folder...)
2. it is hard to distinguish between binary `.cpp` files and unit test files, 
unless  some other "standard" is imposed, such as naming `tests.cpp` (but what about multiple tests then?)

The reason for `include/` folder is:

1. this is classic organization, c'mon!!!
2. this is necessary to isolate header only library and make it easier for others to include them... if you don't want to offer a header only library, ok then, just put everything on `src/` folder and that is fine!

These things can be easily changed, either manually on [cxxbuild.py](cxxbuild.py) script, or by opening an issue and we discuss if some other option is really necessary... 
Note that this project does not aim to have many personalizations and complications, let's use KISS method!

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

### Ongoing extensions for cxxdeps
Some ongoing extensions will allow managing dev dependencies, 
such as build systems (cmake, bazel, etc) and C/C++ package managers (conan, etc), all automatically on `cxxdeps.txt` (or exclusively on `cxxdeps.dev.txt`):
```
cmake == *          [ cmake ]       pip dev [ ninja ]
ninja:windows == *  [ ninja ]       choco dev
ninja:linux == *    [ ninja-build ] apt dev
bazel:windows == *  [ bazelisk ]    choco dev 
bazel:linux == *    [ bazelisk ]    npm dev 
conan == *          [ conan ]       pip dev
```

Note that we can support triplet package notation on project name, 
so as different system package managers (such as apt on ubuntu/debian).
Some package dependency notation can be useful as well to orchestrate installation
flow, when necessary (as an example, ninja could be forcefully installed before cmake).

Other extension is some `build` section... similar to `dev`, but it installs automatically
before build process. The `build` can be seen as a *mandatory* `dev` dependency.
Some *configure* actions and *patches* could also happen in `build` phase 
(which are in fact some *pre-build* actions).

cxxdeps is a cool thing!
- In fact, this was the most motivating part of this project, so feel free to check more painful experiences directly on [manydeps-gmp](https://github.com/manydeps/manydeps-gmp) project!

### Writing cxxdeps in `.toml` format

It is currently possible to write `cxxdeps.toml` file, that automatically generates `cxxdeps.txt` and `cxxdeps.dev.txt` files. Some users may find this easier to understand:

```toml
[all]
fmt={ git="https://github.com/fmtlib/fmt.git", tag="9.1.0", links=["fmt"] }
m={ links=["m"] }
pthread={}

[test]
catch2={ git="https://github.com/catchorg/Catch2.git", tag="v3.3.1", links=[
    "Catch2::Catch2WithMain"
] }

[dev]
bazel=[{ choco=["bazelisk"], platform="windows" }, { npm=["bazelisk"], platform="linux" }]
ninja=[{ choco=["ninja"], platform="windows" }, { apt=["ninja-build"], platform="linux" }]
cmake={ pip=["cmake"], deps=["ninja"] }
conan={ pip=["conan"] }
```

Here one can find sections `all` (equivalent to `*`), `test` and `dev`.
This example install system libraries `-lm` and `-lpthread` for runtime dependencies (`all`),
`catch2` test library linked with cmake `Catch2::Catch2WithMain`, and defines several dev packages.

Check an example in project3 with: `python3 cxxbuild.py demo/project3`

### Drawbacks

None that I know, yet :)

Some people may dislike the imposed organization, like `src/` and `tests/`, but it can be changed manually on script. The idea here is to really make a simplistic script, that really works with highly complex setups (such as taking dependencies from remote and dealing with build systems like cmake and bazel). These things are hard to do even for some experienced c++ programmers... so, as long as it is simple and it works, that is fine! If it doesn't work, file an issue!

## Related Works

- See [ccbuild from debian](https://packages.debian.org/pt-br/sid/devel/ccbuild)
- See [Mantle project](https://github.com/jpxor/Mantle) (experimental but with similar ideas)

None of them support dependencies, such as `cxxdeps.txt`, or even build systems such as cmake and bazel.

Hopefully, when this project is fully finished, C++ will be a better place for all of us :)


## Acknowledgements

Thanks for those trying to use and improve this software.
Specially, thanks Fellipe Pessanha for early suggesting integrating toml support for cxxdeps.

### Citation

```
Igor Machado Coelho. (2023). cxxbuild project. Zenodo. https://doi.org/10.5281/zenodo.10447208
```

## License

Dual licensed: Creative Commons Attribution 4.0 International OR MIT License

Copyleft 2023 

Igor Machado Coelho

