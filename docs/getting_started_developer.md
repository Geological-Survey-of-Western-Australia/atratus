# Developer start up guide

This section covers:

- Downloads required
- Clone the repository locally
- Setup for python virtual environment
- installing cygnets see [guide](cygnet_installation_and_use.md)
- Unit Tests

### Downloads
Several programs and downloads are required to access and use the repository

- Desired IDE/text editor, eg. Visual Studio Code
    - https://code.visualstudio.com/download

- Python, 3.11 is currently being used within the project. The 64 bit version is required for several of the used packages (Windows)
    - https://www.python.org/downloads

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

Once in the environment pip install the requirements. Check this worked correctly by navigating to `./venv/Lib/site-packages` to see all the packages have been installed.
```
pip install -r requirements.txt
```

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