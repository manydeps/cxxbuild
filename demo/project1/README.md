## Demo/Project1

This project demonstrates how a simple project, with a main() on `demo1.cpp`, and two more files `something.h` and `something.cpp`, all hosted on folder `src/`, is very easy to build.
Some tests are hosted on folder `tests/`.
There is also some `lista01` header-only library hosted on `include/` folder, and some dependencies on `cxxdeps.txt`, namely:

- fmt library (from git repository https://github.com/fmtlib/fmt.git)
- Catch2 (from git repository https://github.com/catchorg/Catch2.git)
- pthread system library (on all systems except windows, see triplet `!windows`)
- crypto system library (on linux systems only, see triplet `linux`)

See details on [cxxdeps.txt](cxxdeps.txt):
```
fmt == "9.1.0"     [ fmt ]                    cmake+git *    https://github.com/fmtlib/fmt.git
fmt == "9.1.0"     [ fmt ]                    bazel+bcr *
Catch2 == "v3.5.1" [ Catch2::Catch2WithMain ] cmake+git test https://github.com/catchorg/Catch2.git
catch2 == *        [ catch2_main ]            bazel+git test https://github.com/catchorg/Catch2.git f981c9cbcac07a2690e5a86767eba490b5465463
pthread:!windows
crypto:linux
```

### How to build

Install cxxbuild with: `pip install cxxbuild`

#### For CMake
Just type: `cxxbuild .`

The file `CMakeLists.txt` will be generated automatically.

Output will be built on `build/demo1` and tests on `build/my_test`

#### For Bazel
Just type: `cxxbuild . --bazel`

The files `MODULE.bazel` and `BUILD.bazel` will be generated automatically.

Output will be built on `bazel-bin`, as usual with `bazel build ...`

### License

MIT License


