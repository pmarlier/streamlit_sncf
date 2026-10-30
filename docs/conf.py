# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Streamlit_SNCF"
copyright = "2026, Pierre MARLIER, Ulysse PERRUCHON-MONGE, Christophe VANDENBORRE"
author = "Pierre MARLIER, Ulysse PERRUCHON-MONGE, Christophe VANDENBORRE"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
autoapi_dirs = ["../src"]
autoapi_type = "python"
# autoapi_template_dir = "_templates/autoapi"
extensions = ["autoapi.extension", "sphinx.ext.napoleon"]   # Napoleon handles 
                                                            # docstrings formatting
# extensions = ["sphinx.ext.autodoc"]

# templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "nature"
