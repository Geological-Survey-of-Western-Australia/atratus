# Developer start up guide

This section covers:

- Downloads required
- Clone the repository locally
- Setup for python virtual environment
- Creating an editable install
- Unit Tests

### Downloads
Several programs and downloads are required to access and use the repository

- Desired IDE/text editor, eg. Visual Studio Code
    - Presently raise a service now ticket.

- Python, 3.11 is currently being used within the project. The 64 bit version is required for several of the used packages (Windows)
    - https://www.python.org/downloads
    - if you can't install this raise a service now ticket.

### Clone the repository
clone the repository locally, this can be done through devops, github desktop or vs code. 

### Virtual Environment Setup
Set the execution policy to the current user and the policy to remote signed.
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Create the virtual environment at the location "./venv"
```
python -m venv ./.venv
```

Activate the virtual environment by navigating to the activate file in the following location. 
```
./.venv/Scripts/activate
```
## Setting Up an editable Install
During the development process we want to ensure that the functionality we're prototyping works, within the module. To achieve this we use an editable install with pip. 

To achieve we complete three pip installs we run three commands in command promp in our git directory:
```
# activate our envioronment
> ./.venv/Scripts/activate # activate our venv

# install our requirements + any new dependencies we might be testing
> pip install -r requirements.txt

# perform an editable install, which tells our venv to track chaned models.
> pip install -e .
```
**NOTE - If you use jupyter notebooks in the development process you may need to routinely restart the kernel so any edits can be loaded into the kernel session.**

### Unit tests
This project uses the pytest framework for testing and pytest-cov for coverage reporting. The tests can be run by navigating to the testing side tab of vscode, or via comandline as below. 

```
python -m pytest .\tests\
```

With the .venv active running the line below generates the coverage report, which works well with the vscode extension coverage gutters in watch mode. 
When used well test coverage can be highly useful in developing good meaningful test suite.

While it is tempting to aim for high coverage, what is more important is the development of robust tests that ensure functionality and facilitate the reliability of the code.

```
pytest --cov-report xml:tests\cov.xml --cov atratus
```


***
[Back to Summary](../readme.md)