# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import sphinx_rtd_theme
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------
project = 'frewpy'
copyright = '2020, Fred White'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
    'm2r',
]

source_suffix = ['.rst', '.md']
version = '0.0.0'
author = 'Fred White'

# -- HTML theme settings---- -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    # 'style_external_links': False,
    # 'vcs_pageview_mode': '',
    # 'style_nav_header_background': 'white',
    # Toc options
    # 'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 2,
    # 'includehidden': True,
    # 'titles_only': False
}
