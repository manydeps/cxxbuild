// SPDX-License-Identifier:  MIT
// Copyright (C) 2025 - Prof. Igor Machado Coelho

#ifndef LISTA01_GET_DATA_HPP_
#define LISTA01_GET_DATA_HPP_

#include <string>
#include <print>
#include <format>

std::string get_ij() {
  std::string s = std::format("i={} j={}", 10, 20.5);
  return s;
}

#endif  // LISTA01_GET_DATA_HPP_
