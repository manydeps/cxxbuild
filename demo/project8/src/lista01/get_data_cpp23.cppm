// SPDX-License-Identifier:  MIT
// Copyright (C) 2025 - Prof. Igor Machado Coelho

export module lista01.get_data_cpp23;
import std;

export std::string get_ij() {
  std::string s = std::format("i={} j={}", 10, 20.5);
  return s;
}
