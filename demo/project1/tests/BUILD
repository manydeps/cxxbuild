load("@rules_cc//cc:defs.bzl", "cc_library", "cc_test")
package(default_visibility = ["//visibility:public"])
#
test_suite(
    name = "suite-tests",
    tests = [
        "all_tests"
    ]
)

cc_test(
    name = "all_tests",
    srcs = glob([
		"tests/my_test.cpp",
    ]),
	deps = ["//:my_headers0","@fmt//:fmt","@catch2//:catch2_main",]
)