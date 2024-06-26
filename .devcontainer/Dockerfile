FROM mcr.microsoft.com/devcontainers/cpp:0-ubuntu-22.04

# REFRESH!
RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y

# install pip (for cpplint and cmake)
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends python3-pip

# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends cmake 
RUN pip install --upgrade cmake

# command 'add-apt-repository'
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends software-properties-common

# clang newer
#RUN bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"
RUN curl --proto '=https' --tlsv1.2 https://apt.llvm.org/llvm.sh -sSf | bash -s -- -y

# clangd, clang-format and clang-tidy
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends clang-tidy-18 clang-format-18 clangd-18

# libc++ for clang (not using libstdc++ from gcc)
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends libc++-18-dev libc++abi-18-dev

# install gcc 13 (latest)

# RUN sudo add-apt-repository ppa:ubuntu-toolchain-r/ppa -y
RUN sudo add-apt-repository ppa:ubuntu-toolchain-r/test -y
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends g++-13 gcc-13

# FORCE UPGRADE
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y upgrade

# ===========

# install nvm (for npm)
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
RUN bash /root/.nvm/install.sh

# install npm (using nvm)
RUN bash -i -c "nvm install --lts"

# bazel (using npm)
RUN bash -i -c "npm install -g @bazel/bazelisk"
RUN bash -i -c "npm install -g @bazel/buildifier"

# install cpplint into /usr/local/bin/cpplint
RUN python3 -m pip install cpplint 

# bumpver (for versioning)
RUN python3 -m pip install bumpver

# default gcc-12
RUN sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-13 10
RUN sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-13 10
# default clang-18
RUN sudo update-alternatives --install /usr/bin/clang clang /usr/bin/clang-18 10
RUN sudo update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-18 10
RUN sudo update-alternatives --install /usr/bin/clang-format clang-format /usr/bin/clang-format-18 10
RUN sudo update-alternatives --install /usr/bin/clangd clangd /usr/bin/clangd-18 10
RUN sudo update-alternatives --install /usr/bin/clang-tidy clang-tidy /usr/bin/clang-tidy-18 10

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends python3.10-venv