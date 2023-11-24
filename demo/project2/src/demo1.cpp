// SPDX-License-Identifier:  MIT
// Copyright (C) 2023 - Prof. Igor Machado Coelho
//
// Online test: https://godbolt.org/z/dGfMGzGeW
//
#include <format>
//
// #include <fmt/core.h>
// using fmt::print;
//
#include <lista01/get_data.hpp>

#include "something.h"

// Solution using __VA_ARGS__ and VA_OPT (## from c++20)
#define print(fmt, ...) \
  printf("%s", std::format(fmt, ##__VA_ARGS__).c_str())

int main() {
  print("{} {}! Curso em C/C++\n", "Olá", "Mundo");
  //
  return 0;
}

// Ctrl+Shift+P
// CMake: build
// CMake: configure
// CMake: debug
// [aplicacao]
