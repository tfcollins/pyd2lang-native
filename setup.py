import platform
import os
import toml
from setuptools import setup, find_packages
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
from packaging import tags

with open("pyproject.toml", "r") as f:
    pyproject = toml.load(f)

# Determine OS and architecture specific tags
os_name = platform.system().lower()
arch = platform.machine().lower()

library_name = "d2lib"
if os_name == "windows":
    library_ext = ".lib"
    plat_name = "win_amd64" if arch == "amd64" else "win32"
elif os_name == "linux":
    library_ext = ".so"
    plat_name = "manylinux1_x86_64" if arch == "x86_64" else "manylinux1_i686"
elif os_name == "darwin":
    library_ext = ".dylib"
    # Generate macOS platform tags
    macos_version = platform.mac_ver()[0].split('.')
    macos_major = macos_version[0]
    macos_minor = macos_version[1]
    plat_name = f"macosx_{macos_major}_{macos_minor}_{arch}"
else:
    raise ValueError(f"Unsupported OS: {os_name}")

library_filename = f"{library_name}{library_ext}"

this_folder = os.path.dirname(os.path.abspath(__file__))
library_path = os.path.join(this_folder, "d2", "resources", library_filename)
if not os.path.exists(library_path):
    raise FileNotFoundError(f"Library file not found: {library_path}")

class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        self.plat_name_supplied = True
        self.plat_name = plat_name
        super().finalize_options()

setup(
    name=pyproject["project"]["name"],
    version=pyproject["project"]["version"],
    description=pyproject["project"]["description"],
    classifiers=[
        f"Operating System :: {os_name}",
        f"Architecture :: {arch}",
    ],
    package_data={
        "d2": [os.path.join("resources", library_filename)],
    },
    include_package_data=True,
    cmdclass={
        'bdist_wheel': bdist_wheel,
    },
)
