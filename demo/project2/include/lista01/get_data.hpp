// SPDX-License-Identifier:  MIT
// Copyright (C) 2023 - Prof. Igor Machado Coelho

#ifndef LISTA01_GET_DATA_HPP_
#define LISTA01_GET_DATA_HPP_

#include <format>
#include <fstream>
#include <iostream>
#include <string>
//
// #include <fmt/core.h>
// using fmt::format;

std::string get_ij() {
  std::string s = std::format("i={} j={}", 10, 20.5);
  return s;
}

std::string get_data() {
  std::cout << "open file! " << std::endl;

  std::ifstream ifs("resources/hello.txt");
  using It = std::istreambuf_iterator<char>;
  return std::string(It(ifs), It());
}

#endif  // LISTA01_GET_DATA_HPP_
