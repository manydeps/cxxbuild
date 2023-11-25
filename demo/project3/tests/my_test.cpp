// SPDX-License-Identifier:  MIT
// Copyright (C) 2023 - Prof. Igor Machado Coelho

#include <catch2/catch_all.hpp>
//
#include <lista01/get_data.hpp>

TEST_CASE("Teste1") {
  // WRONG test (will FAIL)
  int x = 10;
  REQUIRE(x == 12);
}

TEST_CASE("Teste2") {
  // GOOD test (will PASS)
  REQUIRE(get_ij() == "i=10 j=20.5");
}
