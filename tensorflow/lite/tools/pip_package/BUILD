load("//tensorflow/lite/tools/pip_package:utils/py_wheel.bzl", "py_wheel")

package(default_visibility = ["//visibility:private"])

py_binary(
    name = "wheel_builder",
    srcs = [
        "wheel_builder.py",
    ],
    main = "wheel_builder.py",
    deps = [
        "@pypi_setuptools//:pkg",
    ],
)

genrule(
    name = "setup_py",
    srcs = ["//tensorflow/lite/tools/pip_package:setup_with_binary.py"],
    outs = ["setup.py"],
    cmd = "cat $< > $@",
)

py_wheel(
    name = "litert_wheel",
    srcs = [
        "//tensorflow/lite/profiling/proto:model_runtime_info_py",
        "//tensorflow/lite/profiling/proto:profiling_info_py",
        "//tensorflow/lite/python:schema_py",
        "//tensorflow/lite/python/interpreter_wrapper:_pywrap_tensorflow_interpreter_wrapper",
    ],
    platform_name = "manylinux_2_17_x86_64",
    pyproject = ":setup_py",
)
