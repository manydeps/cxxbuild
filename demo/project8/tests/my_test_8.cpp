// SPDX-License-Identifier:  MIT
// Copyright (C) 2025 - Prof. Igor Machado Coelho

import boost.ut;
import lista01.get_data_cpp23;

auto main() -> int {
  using namespace boost::ut;

  "Teste10"_test = [] {
    int x = 10;
    expect(x == 10);
  };

  return 0;
}
