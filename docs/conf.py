import importlib.util
import os
import re
import sys

# Extract version from d2/__init__.py without importing the module
# (importing requires the native .so which isn't available in docs CI)
_version_file = os.path.join(os.path.abspath(".."), "d2", "__init__.py")
_version = "0.0.0"
with open(_version_file) as f:
    for line in f:
        m = re.match(r'^__version__\s*=\s*["\']([^"\']+)["\']', line)
        if m:
            _version = m.group(1)
            break

# Only add d2 to sys.path if the native library is loadable
if importlib.util.find_spec("d2") or os.path.exists(
    os.path.join(os.path.abspath(".."), "d2", "resources")
):
    sys.path.insert(0, os.path.abspath(".."))

project = "pyd2lang-native"
copyright = "2024, Travis F. Collins"
author = "Travis F. Collins"
version = _version
release = _version

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "d2.sphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build"]

html_theme = "furo"
html_title = "pyd2lang-native"
html_logo = "_static/logo.svg"

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#0067B9",
        "color-brand-content": "#004A87",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4D9AD5",
        "color-brand-content": "#A8D4F0",
    },
    "source_repository": "https://github.com/tfcollins/pyd2lang-native",
    "source_branch": "main",
    "source_directory": "docs/",
}

html_static_path = ["_static"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

autodoc_member_order = "bysource"
