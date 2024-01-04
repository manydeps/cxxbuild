## Demo/Project2

This project demonstrates how a very simple project, with a main() on `demo2.cpp`, and two more files `something.h` and `something.cpp`, all hosted on folder `src/`, is very easy to build.

No more extra dependencies are provided in this example.

### How to build

Install cxxbuild with: `pip install cxxbuild`

#### For CMake
Just type: `cxxbuild .`

The file `CMakeLists.txt` will be generated automatically.

Output will be built on `build/demo2`

#### For Bazel
Just type: `cxxbuild . --bazel`

The files `MODULE.bazel` and `BUILD.bazel` will be generated automatically.

Output will be built on `bazel-bin`, as usual with `bazel build ...`

### License

MIT License
 

