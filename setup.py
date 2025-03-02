from setuptools import setup, Extension
from setuptools.command.bdist_wheel import bdist_wheel as _bdist_wheel
import platform
import os
import toml

with open("pyproject.toml", "r") as f:
    pyproject = toml.load(f)

# Determine OS and architecture specific tags
os_name = platform.system().lower()
arch = platform.machine().lower()

library_name = "d2lib"
if os_name == "windows":
    library_ext = ".dll"
    plat_name = f"win_{arch}"
elif os_name == "linux":
    library_ext = ".so"
    plat_name = f"linux_{arch}"
elif os_name == "darwin":
    library_ext = ".dylib"
    plat_name = f"macos_{arch}"
else:
    raise ValueError(f"Unsupported OS: {os_name}")

library_filename = f"{library_name}{library_ext}"


class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        self.plat_name_supplied = True
        self.plat_name = plat_name
        super().finalize_options()


setup(
    classifiers=[
        f"Operating System :: {os_name}",
        f"Architecture :: {arch}",
    ],
    package_data={"d2": [os.path.join("resources", library_filename)]},
    include_package_data=True,
    cmdclass={"bdist_wheel": bdist_wheel},
)
