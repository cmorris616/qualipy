# Getting Started
{{projectDescription}}
## Initial Setup
**In order to test using JIRA, you must have a running JIRA instance.  {{projectName}} will run without project management software.**
1. Create a test project that uses **behave** to run tests from feature files
1. Create and activate a virtual environment (optional)
1. Install {{projectName}} (**pip install {{packageName}}**)
1. Execute {{projectName}} (**python -m {{packageName}}**)

QualiPy looks for **qualipy.yaml** in the current directory.  If that is not found, then default configuration settings are used.  Additionally, other YAML config files can be used by including the **&dash;&dash;config-file** command line argument. 

QualiPy assumes that the feature files are located in the **features** directory in the current working directory.  This can be changed with the **&dash;&dash;features-dir** command line argument.

## Command Line Arguments
- &dash;&dash;config-file *&lt;path to file&gt;*[settings](settings.md)
    - The path to the YAML file that contains the configuration settings (see )
    - **Default:** ./qualipy.yaml
    - If no config file is available, QualiPy will run with default settings
- &dash;&dash;features-dir *&lt;path to folder&gt;*
    - The path to the folder containing the feature files for the project
    - **Default:** ./features
- &dash;&dash;output-dir *&lt;path to folder&gt;*
    - The location in which output files will be saved
    - **Default:** ./qualipy_output