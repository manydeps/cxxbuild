## Demo/Project6 (cmake only)

This project demonstrates how complex dependencies can be added.
We test:

- google abseil library (`absl`)
- optframe framework (`optframe`)

For linux, run `./get_optframe.sh` to load it locally with `cxxdeps.txt`!
On Windows, it will follow `cxxdeps.windows.txt` automatically, instead of `cxxdeps.txt`.

These work for both c++17 (default) and c++20

### How to build

Install cxxbuild with: `pip install cxxbuild`

#### For CMake
Just type: `cxxbuild .`

The files `CMakeLists.txt` and `cxxdeps.txt` will be generated automatically.

Output will be built on `build/demo6`

### License

MIT License




