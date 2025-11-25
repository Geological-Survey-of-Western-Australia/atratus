# Contributing
- [Introduction](#introduction)
- [Code of Conduct](#code-of-conduct)
- [How to contribute](#how-to-contribute)
- [Getting started](#getting-started)
- [Coding Guidelines](#coding-guidelines)

## Introduction

Thank you for considering contributing to the gswa-atratus! Contributions are welcomed and encouraged. This document details the contribution process.

Atratus is a tool to faciltate geoscience data processing pipelines and harmonisation. This tool provides abstract base clases, centralises logging, and database interactions!

As it stands, Atratus is stable enough to use to generate facilitate the basics. That being said, some great contributions to the Atratus project would include:
- Improved logging reporting including dashboards and more effective collation.
- Support of Array and geometry type data fields in databases.

## Code of Conduct

This project follows the [DMPE Code of Conduct](https://www.wa.gov.au/organisation/department-of-mines-petroleum-and-exploration/careers-dmpe-living-our-values). By contributing, you agree to uphold this code. Please report unacceptable behaviour to [gdi.contact@dmpe.wa.gov.au](mailto:gdi.contact@dmpe.wa.gov.au?subject=Atratus%20behaviour). Please be respectful and constructive in all interactions.

## How to contribute

### Report a bug

Please let us know if something is not working as expected. If you have identified a security vulnerability report it directly to [gdi.contact@dmpe.wa.gov.au](mailto:gdi.contact@dmpe.wa.gov.au?subject=Atratus%20vulnerability). 

**Before reporting a bug** 
- Make sure you are using the latest version/are using code from the main branch.
- Ensure the issue is not due to incompatible environments or dependencies. Read the [documentation](#link) to ensure your environment is compatible.
- Check [GitHub issues](https://github.com/Geological-Survey-of-Western-Australia/atratus/issues) to see if the bug has already been reported. If a similar open issue has already been raised, please add it as a comment rather than making a new issue.

**When reporting a bug**
- If you cannot find an open issue describing the problem, please [open a new one](https://github.com/Geological-Survey-of-Western-Australia/atratus/issues/new/choose). 
- Provide a clear and descriptive title.
- Outline the expected versus actual behaviour. Include steps to reproduce the bug.
- Include OS, platform, and package details.
- Include error messages and screenshots when useful. 

### Suggest a new feature/enhancement

Please let us know if there are additional features or enhancements to the code that can improve [this project].

**Before suggesting a new feature/enhancement** 
- Make sure you are using the latest version/are using code from the main branch.
- Read the [documentation](#link) to ensure the feature/enhancement has not been implemented.
- Check [GitHub issues](https://github.com/Geological-Survey-of-Western-Australia/atratus/issues) to see if the feature/enhancement has already been suggested. 

When suggesting a feature, provide a clear and descriptive title, and explain how the suggestion improves the project. Describe the current behaviour of the code, and how the suggestion would change it. Provide examples and use cases when useful.

### Patch a bug or implement a new feature/enhancement

To contribute code to [the project] open a new GitHub pull request. Ideally each patch should be linked with a bug identified in [GitHub issues](link).

**When contributing code** 
- Ensure that the PR description has a clear and descriptive title.
- Identify the bug or new feature/enhancement in in [GitHub issues](https://github.com/Geological-Survey-of-Western-Australia/atratus/issues). If there is not yet an issue for your contribution, please open a new issue and link it with your PR.
- Describe your change and how it addresses a known bug, improves performance, or enhances Atratus.
- Explain alternate designs, and why the proposed change was selected
- Describe potential drawbacks or impacts of the change.
- Describe the verification process to ensure bugs weren't introduced.

## Getting started

### Which branch to use

[Describe branches, and which is the main branch contributors should use]

### Setting up a development environment

To contribute to this project, please follow the steps below to set up a local development environment:

1. Clone the repository and download the project to your local machine using Git:
    ```
    git clone https://github.com/Geological-Survey-of-Western-Australia/atratus.git
    cd your-repo-name
    ```

2. Create an environment and install dependencies

    ```
    conda create -n your-environment-name -f environment.yaml
    conda activate your-environment-name
    ```
    or (depending on availability of `environment.yaml` or `pyproject.toml`)
    ```
    pip install pyproject.toml
    ```

### GitHub Issues

[GitHub issues](https://github.com/Geological-Survey-of-Western-Australia/atratus) is the primary method for tracking changes and updates to [the project]. [X] tags are available when making a submitting to [GitHub issues](link):
- **discussion (code):** These are inquiries regarding the functionality of the code. Depending on the inquiry, these can become **bug** or **new feature/enhancement** issues.
- **discussion (geoscience):** These are inquiries regarding the geoscience and research aspects of the project. Depending on the inquiry, these can become **bug** or **new feature/enhancement** issues.
- **proposal:** These are suggestions for new ideas or functionality that require larger discussions with [project members]. A proposal can become a **new feature/enhancement** 
- **bug:** These track issues with the code. Any security vulnerability should be reported directly to  [gdi.contact@dmpe.wa.gov.au](mailto:gdi.contact@dmpe.wa.gov.au?subject=atratus%20vulnerability).
- **new feature/enhancement:** These track specific features or enhancements requests.

### Pull Requests

We welcome contributions via pull requests (PRs). To help maintain code quality and consistency, please follow these guidelines when submitting a PR:

**How to Format Your Pull Request**

Use a clear and descriptive title that summarizes the purpose of the PR.
In the PR description, include:
- A brief overview of the changes made.
- The issue number(s) the PR addresses (if applicable).
- The motivation for the change and its expected impact.
- Any alternative approaches considered.
- Any known limitations or side effects.

**Testing and Verification**

[How are we testing?]

If your changes affect functionality, include or update unit tests where applicable. Verify that your changes do not break existing functionality.
If your contribution includes new features, consider adding example usage or updating relevant documentation.

**Review Process**

Once submitted, your PR will be reviewed by a maintainer. You may be asked to make changes or clarify aspects of your contribution. Please be responsive to feedback and open to discussion.

### Style guide

This project uses the PEP 8 style guide to ensure consistency and readability across the project. Contributors are encouraged to write clear, descriptive docstrings for all functions and classes, and to use comments where necessary to explain code decisions. Well-documented code helps others understand and build upon your work, and is essential for maintaining quality in collaborative projects.
