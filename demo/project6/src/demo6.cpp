#include <iostream>
//
#include <OptFrame/printable/printable.hpp>
//
#include <OptFCore/FCore.hpp>
//
#include "inctest/file.hpp"

int main() {
  std::cout << optframe::FCore::welcome() << std::endl;
  std::cout << hello() << std::endl;

  return 0;
}
