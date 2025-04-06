## Demo/Project7 (similar to Project3) C++23 - cmake-only

This project demonstrates how a simple `C++23` project, with a main() on `demo7.cpp` hosted on folder `src/`, is very easy to build.
This is a CMake-only simplification of Project3 (no bazel here!).
Some tests are hosted on folder `tests/`.
There is also some `lista01` header-only library hosted on `include/` folder, and some dependencies on `cxxdeps.toml` (the difference to Project1, is that this one uses `toml` format instead of `txt`), namely:

- this demonstrates `<print>` from C++23
- ut (from git repository https://github.com/boost-ext/ut.git)

At least GCC 14 is required, so recommended flag to force compiler may be needed:

- `uv run cxxbuild demo/project7 --c++23 --compiler "/usr/bin/g++-14"`

### How to build

Install cxxbuild with: `pip install cxxbuild`

#### For CMake
Just type: `cxxbuild . --c++23 --compiler "/usr/bin/g++-14"`

The files `CMakeLists.txt` and `cxxdeps.txt` will be generated automatically.

Output will be built on `build/demo7` and tests on `build/my_test_7_test`

### License

MIT License




