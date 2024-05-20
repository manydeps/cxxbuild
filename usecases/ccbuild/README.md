## cxxbuild usecase: ccbuild

Trying to build project: https://github.com/bneijt/ccbuild

Steps:

- Download .zip: `wget https://github.com/bneijt/ccbuild/archive/refs/heads/main.zip`
- Unzip it: `unzip main.zip`
- Manually install dependencies from `cxxdeps.template.txt`
- Copy cxxdeps: `cp cxxdeps.template.txt ccbuild-main/cxxdeps.txt`
- Invoke cxxbuild on ccbuild-main folder: `cxxbuild ccbuild-main`
- Manually fix the FLEX on generated CMakeLists, as discussed before, by adding two extra lines on cmakelists (see example)
- Manually invoke cmake to finish build: `cd ccbuild-main/build/ && cmake .. -GNinja && ninja`
- Still not fully automated, but it works!

See issue: https://github.com/bneijt/ccbuild/issues/34
