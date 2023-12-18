# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Python_fixtures'
copyright = '2023, GMC'
author = 'GMC'
import sphinx_rtd_theme

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_rtd_theme'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_theme_options = {
    'logo_only': False,
    'display_version': False,  # False so doc version not shown
    'prev_next_buttons_location': 'both',  # Can be bottom, top, both , or None
    'style_external_links': True,  # True to Add an icon next to external links
    'style_nav_header_background': 'linear-gradientlinear-gradient(to right, blueviolet 15%, limegreen 50%, royalblue 80%)',  # blue
    # Toc options
    'collapse_navigation': False,  # False so nav entries have the [+] icons
    'sticky_navigation': False,  # False so the nav does not scroll
    'navigation_depth': 4,  # -1 for no limit
    'includehidden': True,  # displays toctree that are hidden
    'titles_only': False  # False so page subheadings are in the nav.
}