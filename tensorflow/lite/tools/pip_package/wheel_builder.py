# Copyright 2025 The Tensorflow Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TODO: sosagarcia - DO NOT SUBMIT without one-line documentation for wheel_builder.

TODO: sosagarcia - DO NOT SUBMIT without a detailed description of
wheel_builder.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
from typing import Optional


def parse_args() -> argparse.Namespace:
  """Arguments parser."""
  parser = argparse.ArgumentParser(
      description="Helper for building python wheel from pyproject.toml",
      fromfile_prefix_chars="@",
  )
  parser.add_argument("--pyproject", help="location of pyproject.toml file")
  parser.add_argument("--setup_py", help="location of setup.py file")
  parser.add_argument(
      "--src", help="single source file for the wheel", action="append"
  )
  parser.add_argument(
      "--platform",
      required=True,
      help="Platform name to be passed to build module",
  )
  return parser.parse_args()


def get_project_name(pyproject_path: str) -> str:
  with open(pyproject_path, "rb") as f:
    pyproject = tomllib.load(f)
    try:
      return pyproject["project"]["name"]
    except KeyError as e:
      raise ValueError(
          "Invalid pyproject.toml file. Please check the project name."
          " Dynamically generated project names are not supported."
      ) from e


def prepare_build_tree(tree_path, args, project_name: str):
  """Prepares the build tree for the wheel build.

  Args:
    tree_path: Path to the build tree.
    args: Command line arguments.
    project_name: Name of the project.
  """
  src_dir = os.path.join(tree_path, project_name.replace("-", "_"))
  os.makedirs(src_dir, exist_ok=True)

  if args.pyproject:
    shutil.copyfile(
        arg_data.pyproject, os.path.join(tree_path, "pyproject.toml")
    )
  else:
    shutil.copyfile(arg_data.setup_py, os.path.join(tree_path, "setup.py"))

  for src in arg_data.src:
    shutil.copyfile(src, os.path.join(src_dir, os.path.basename(src)))


def build_pyproject_wheel(
    buildtree_path: str, platform_name: Optional[str] = None
):
  """Builds a python wheel from a pyproject.toml file.

  Args:
    buildtree_path: Path to the build tree.
    platform_name: Platform name to be passed to build module.
  """
  env = os.environ.copy()

  command = [
      sys.executable,
      "-m",
      "build",
      "-w",
      "-o",
      os.getcwd(),
  ]

  if platform_name:
    command.append(
        # This is due to setuptools not making it possible to pass the
        # platform name as a dynamic pyproject.toml property.
        f"--config-setting=--build-option=--plat-name={platform_name}"
    )

  subprocess.run(
      command,
      check=True,
      cwd=buildtree_path,
      env=env,
  )


def build_setup_py_wheel(
    buildtree_path: str, platform_name: Optional[str] = None
):
  """Builds a python wheel from a setup.py file.

  Args:
    buildtree_path: Path to the build tree.
    platform_name: Platform name to be passed to build module.
  """
  env = os.environ.copy()

  command = [
      sys.executable,
      "tensorflow/tools/pip_package/setup.py",
      "bdist_wheel",
      f"--dist-dir={os.getcwd()}/dist",
      f"--plat-name={platform_name}",
  ]

  subprocess.run(
      command,
      check=True,
      cwd=buildtree_path,
      env=env,
  )


if __name__ == "__main__":
  tmpDir = tempfile.TemporaryDirectory(prefix="ai_edge_litert_wheel")
  tmpDir_path = tmpDir.name

  arg_data = parse_args()
  prepare_build_tree(tmpDir_path, arg_data, "ai_edge_litert")
  build_setup_py_wheel(tmpDir_path, arg_data.platform)

  tmpDir.cleanup()
