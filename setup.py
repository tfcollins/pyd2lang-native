from setuptools import setup, find_packages
from setuptools.dist import Distribution

class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

if __name__ == "__main__":
    setup(
        distclass=BinaryDistribution,
        # Read metadata from pyproject.toml
        use_scm_version=False,
    )