import os
import sys

sys.path.insert(0, os.path.abspath(".."))

import d2

project = "pyd2lang-native"
copyright = "2024, Travis F. Collins"
author = "Travis F. Collins"
version = d2.__version__
release = d2.__version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = ["_build"]

html_theme = "furo"
html_title = "pyd2lang-native"

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
    "source_branch": "dev",
    "source_directory": "docs/",
}

html_static_path = ["_static"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

autodoc_member_order = "bysource"
