load("@rules_cc//cc:defs.bzl", "cc_library", "cc_test")

package(default_visibility = ["//visibility:public"])


cc_test(
    name = "all_tests",
    srcs = glob([
        "my_test.cpp",
    ]),
    deps = ["//:my_include", "@fmt//:fmt", "@catch2//:catch2_main"]
)

test_suite(
    name = "suite-tests",
    tests = [
        "all_tests"
    ]
)
