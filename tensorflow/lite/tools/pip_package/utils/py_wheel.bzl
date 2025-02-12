# Copyright 2025 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TODO: sosagarcia - Write module docstring."""

def _py_wheel_impl(ctx):
    executable = ctx.executable.wheel_binary
    pyproject_file = ctx.file.pyproject
    filelist_lists = [src.files.to_list() for src in ctx.attr.srcs]
    filelist = [f for filelist in filelist_lists for f in filelist]
    output_file = ctx.actions.declare_file("ai_edge_litert-1.1.0-py3-none-any.whl")

    args = ctx.actions.args()
    if ctx.attr.pyproject:
        args.add("--pyproject", pyproject_file.path)

    if ctx.attr.setup_py:
        args.add("--setup_py", setup_py_file.path)

    for f in filelist:
        args.add("--src", f.path)

    if ctx.attr.platform_name:
        args.add("--platform", ctx.attr.platform_name)

    args.set_param_file_format("flag_per_line")
    args.use_param_file("@%s", use_always = False)

    ctx.actions.run(
        arguments = [args],
        inputs = filelist + [pyproject_file],
        outputs = [output_file],
        executable = executable,
    )
    return [DefaultInfo(files = depset(direct = [output_file]))]

py_wheel = rule(
    implementation = _py_wheel_impl,
    attrs = {
        "srcs": attr.label_list(
            allow_files = True,
        ),
        "pyproject": attr.label(
            allow_single_file = [".toml"],
        ),
        "setup_py": attr.label(
            allow_single_file = [".py"],
            mandatory = True,
        ),
        "platform_name": attr.string(),
        "wheel_binary": attr.label(
            default = Label("//tensorflow/lite/tools/pip_package:wheel_builder"),
            executable = True,
            cfg = "exec",
        ),
    },
)
