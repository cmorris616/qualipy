import tomli
from os import path
from datetime import datetime

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

projectTOML_file = path.abspath(path.join(path.dirname(path.abspath(__file__)), '..', '..', 'qualipy', 'pyproject.toml'))

if path.exists(projectTOML_file):
    with open(projectTOML_file, mode='rb') as pt:
        toml = tomli.load(pt)
        release = toml['project']['version']

        author_list = []

        for current_author in toml['project']['authors']:
            author_list.append(current_author['name'])
else:
    copyright = '2023, Charles Morris'
    author_list = ['Charles Morris']
    release = '1.0.1'

project = 'QualiPy'
author = ', '.join(author_list)
copyright = str(datetime.now().year) + ', ' + author

project_description = f'{project} is a framework designed to augment the automated testing process.' \
    f'  Automated testing frameworks handle reading the feature files and running the tests.' \
    f'  {project} handles getting the feature files to the correct location for execution and '\
        'uploading the test results to a project management suite (such as JIRA).'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx_rtd_theme',
    'sphinx.ext.autodoc'
    ]
myst_enable_extensions = ['substitution']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

rst_prolog = f"""
.. |projectName| replace:: {project}
.. |projectDescription| replace:: {project_description}
"""

myst_substitutions = {
    'projectName': project,
    'packageName': project.lower(),
    'projectDescription': project_description
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
