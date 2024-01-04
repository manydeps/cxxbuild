## Demo/Project3 (similar to Project1)

This project demonstrates how a simple project, with a main() on `demo3.cpp`, and two more files `something.h` and `something.cpp`, all hosted on folder `src/`, is very easy to build.
Some tests are hosted on folder `tests/`.
There is also some `lista01` header-only library hosted on `include/` folder, and some dependencies on `cxxdeps.toml` (the difference to Project1, is that this one uses `toml` format instead of `txt`), namely:

- fmt library (from git repository https://github.com/fmtlib/fmt.git)
- Catch2 (from git repository https://github.com/catchorg/Catch2.git)
- pthread system library (on all systems except windows, see triplet `!windows`)
- crypto system library (on linux systems only, see triplet `linux`)


### How to build

Install cxxbuild with: `pip install cxxbuild`

#### For CMake
Just type: `cxxbuild .`

The files `CMakeLists.txt`, `cxxdeps.txt` and `cxxdeps.dev.txt` will be generated automatically.

Output will be built on `build/demo3` and tests on `build/my_test`

#### For Bazel
Just type: `cxxbuild . --bazel`

The files `MODULE.bazel` and `BUILD.bazel` will be generated automatically.

Output will be built on `bazel-bin`, as usual with `bazel build ...`

### License

MIT License




