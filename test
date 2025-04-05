#!/bin/bash

python3 cxxbuild/cxxbuild.py demo/project1
python3 cxxbuild/cxxbuild.py demo/project2
python3 cxxbuild/cxxbuild.py demo/project3
python3 cxxbuild/cxxbuild.py demo/project4 --c++20

python3 cxxbuild/cxxbuild.py demo/project1 --bazel
python3 cxxbuild/cxxbuild.py demo/project2 --bazel
python3 cxxbuild/cxxbuild.py demo/project3 --bazel
python3 cxxbuild/cxxbuild.py demo/project4 --c++20 --bazel

echo "FINISHED tests"
