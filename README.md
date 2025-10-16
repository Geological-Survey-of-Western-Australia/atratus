## GDI - GeoDigitalTools

*A Common tools for GeoData Handling*
___

# Introduction 
This repository contains code for geoscience data handling and harmonisation, it is developed as part of the core operations of the Geoscience Data Integrations Branch, of the Geological Surevy of Western Australia.

All digital geoscience data requires extremely diverse ETL processes. While the extraction and transformation processes require highly bespoke solutions (cygnets), some utilities should be shared across projects. 

This library is designed to facilitate the loading of tabular data from various projects,centralise logging, and provide a base abstraction to the proccess and steps typical for geodata harmonisation.

This system is intended to support the various geodata harmonisation efforts of the GSWA-GDI team called cygnets. 

## Feature List
 - Basic database operations
 - Error Logging and Handling
 - Cygnet: Data Harmonisation (Process and Steps)

### Acknowledgements
This work would not be made possible without key contributions from members of the GDI team: Luke Smith, Tasman Gillfeather-Clark, and Jianli Zhi. 

### Contact
If you have any questions about the tool you can contact the GDI team here.

gdi.contact@dmpe.wa.gov.au

# Getting Started

### Installation process
This tool is built and distributed via pypi and can be installed with the following command. 
```
pip install geo_digital_tools
```
This tools is largely intended to be used by the various other projects of the GDI team and as such is likely installed simply as a dependency.

Alternatively you can clone the git repository and do an editable install. 

```
git clone
```

### Software dependencies
The packages t`pyproject.toml` or `environment.yaml` or `requirements.txt`.

## Documentation
- [Getting Started for Developers](docs/source/getting_started_developer.rst)
- [General Design & Flow](docs/source/high_level_design.rst)
- [Installation and Use](docs/source/installation_and_use.rst)
- [Logging](docs/source/logging.rst)



[Describe the folder/file structure of the repository]:
1. **file1.py** takes data from [GSWA's Data and Software Centre](https://dasc.dmirs.wa.gov.au/).
2. **file2.py** does an action.
3. **file3.py** contains functions used in file 2.



# Contributing

Contributions to this project are welcome. Please refer to [contributing guide](#link) to learn more about how to contribute.

# Maintenance and Support

This codebase was developed for research purposes and is not actively maintained. If you encounter issues or have suggestions for improvement, feel free to submit them to [GitHub Issues](#link) or via [email](#link). Feedback is appreciated and may inform future work, but any changes will be addressed in a new project, not this one.

# License

[GNU GPL 3.0](https://choosealicense.com/licenses/gpl-3.0/)