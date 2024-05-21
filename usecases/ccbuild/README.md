## cxxbuild usecase: ccbuild

Trying to build project: https://github.com/bneijt/ccbuild

Steps:

- Download .zip: `wget https://github.com/bneijt/ccbuild/archive/refs/heads/main.zip`
- Unzip it: `unzip main.zip`
- Manually install dependencies from `cxxdeps.template.txt`
- Copy cxxdeps: `cp cxxdeps.template.txt ccbuild-main/cxxdeps.txt`
- Copy flex patch file: `cp patch_flex.txt ccbuild-main/`
- Invoke cxxbuild on ccbuild-main folder and be happy: `cxxbuild ccbuild-main`

See issue: https://github.com/bneijt/ccbuild/issues/34
