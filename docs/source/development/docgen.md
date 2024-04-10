# Documentation
The documentation for the project should be kept up to date with the code changes.  The documentation is hosted on readthedocs.org.

## Building the documentation
Sphinx is used to build the documentation.  The source for the documentation is in **docs/source**.  The built documentation should be placed in **docs/build**.  In order to build the documentation, navigate to the docs folder and execute the below commands.

    sphinx-apidoc -o source/apidocs ../qualipy/src/qualipy
    sphinx-build source build