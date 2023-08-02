# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'tensorconvertor'
copyright = '2023, Tianyi Li'
author = 'Tianyi Li'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "autodoc2"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# autodocs
autodoc2_packages = [
    "../src/tensorconvertor",
]
autodoc2_render_plugin = "myst"
autodoc2_module_all_regexes = [
    r"tensorconvertor/..*",
]

# myst
myst_enable_extensions = [
    "dollarmath",
    "fieldlist",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
