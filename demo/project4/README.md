## Demo/Project4 (same as Demo/Project1)

This project demonstrates how a simple project, with a main() on `demo4.cpp`, and two more files `something.h` and `something.cpp`, all hosted on folder `src/`, is very easy to build.
Some tests are hosted on folder `tests/`.

This is the same as Project1, but requiring c++20 instead of c++17 (thus not requiring fmt dependency).

There is also some `lista01` header-only library hosted on `include/` folder, and some dependencies on `cxxdeps.txt`, namely:

- Catch2 (from git repository https://github.com/catchorg/Catch2.git)
- pthread system library (on all systems except windows, see triplet `!windows`)
- crypto system library (on linux systems only, see triplet `linux`)

See details on [cxxdeps.txt](cxxdeps.txt):
```
Catch2 == "v3.5.1" [ Catch2::Catch2WithMain ] cmake+git test https://github.com/catchorg/Catch2.git
catch2 == *        [ catch2_main ]            bazel+git test https://github.com/catchorg/Catch2.git f981c9cbcac07a2690e5a86767eba490b5465463
```

### How to build

Install cxxbuild with: `pip install cxxbuild`

#### For CMake
Just type: `cxxbuild . --c++20`

The file `CMakeLists.txt` will be generated automatically.

Output will be built on `build/demo4` and tests on `build/my_test`

#### For Bazel
Just type: `cxxbuild . --bazel`

The files `MODULE.bazel` and `BUILD.bazel` will be generated automatically.

Output will be built on `bazel-bin`, as usual with `bazel build ...`

### License

MIT License


