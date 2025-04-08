## Demo/Project8 (CXX Modules and `import std;`) C++23 - cmake-only

This project demonstrates how a simple `C++23` project, with a main() on `demo8.cpp` hosted on folder `src/`, is very easy to build.
This is a CMake-only simplification of Project3 (no bazel here!).
Some tests are hosted on folder `tests/`.
There is also some `lista01` header-only library hosted on `include/` folder, and some dependencies on `cxxdeps.toml` (the difference to Project1, is that this one uses `toml` format instead of `txt`), namely:

- this demonstrates `import std;` from C++23
- ut (from git repository https://github.com/boost-ext/ut.git)

At least GCC 15 is required, so recommended flag to force compiler may be needed:

- `uv run cxxbuild demo/project8 --c++23 --compiler "/usr/bin/g++-15" --import std --cmake-unset BOOST_UT_DISABLE_MODULE`

Clang 19 with stdlib libc++ also works (note `gnu++23` instead of `c++23`, because we need extensions):

- `uv run cxxbuild demo/project8 --gnu++23 --compiler "/usr/bin/clang++-19" --stdlib libc++ --import std --cmake-unset BOOST_UT_DISABLE_MODULE`

### How to build

Install cxxbuild with: `pip install cxxbuild`

#### For CMake
Just type: `cxxbuild . --c++23 --compiler "/usr/bin/g++-15" --import std --cmake-unset BOOST_UT_DISABLE_MODULE`

The files `CMakeLists.txt` and `cxxdeps.txt` will be generated automatically.

Output will be built on `build/demo8` and tests on `build/my_test_8_test`

### License

MIT License




