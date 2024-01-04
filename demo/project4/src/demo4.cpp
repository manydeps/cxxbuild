// SPDX-License-Identifier:  MIT
// Copyright (C) 2023 - Prof. Igor Machado Coelho
//
#include <format>
//
#include <lista01/get_data.hpp>

#include "something.h"

// Solution using __VA_ARGS__ and VA_OPT (## from c++20)
#define print(fmt1, ...) \
  printf("%s", std::format(fmt1, ##__VA_ARGS__).c_str())

int main() {
  print("{} {}! Curso em C/C++\n", "Olá", "Mundo");
  print("{}", func1());
  //
  return 0;
}

// Ctrl+Shift+P
// CMake: build
// CMake: configure
// CMake: debug
// [aplicacao]
