# GSWA - Atratus
*Common tools for GeoData Handling and Harmonisation*

## Introduction 
This repository contains code to support geoscience data handling and harmonisation, it is developed as part of the core operations of the Geoscience Data Integrations Branch, of the Geological Survey of Western Australia.

All digital geoscience data requires extremely diverse ETL processes. While the extraction and transformation processes require highly bespoke solutions (cygnets), some utilities should be shared across projects. 

This library is designed to facilitate the **loading of tabular data** from various projects, **centralise logging**, and provide a base abstraction to the **process and steps** typical for geodata harmonisation.

This system is intended to support the various geodata harmonisation efforts of the GSWA-GDI team called cygnets. 


## Getting Started

This tool is built and distributed via pypi and can be installed with the following command. 
```
pip install gswa-atratus
```
This tools is largely intended to be used by the various other projects of the GDI team and as such is likely installed simply as a dependency.

Alternatively you can clone the git repository and do an editable install. 

```
git clone https://github.com/Geological-Survey-of-Western-Australia/atratus.git
```

## Maintenance and Support
This codebase was developed for research purposes and is maintained. If you encounter issues or have suggestions for improvement, feel free to submit them to [GitHub Issues](https://github.com/Geological-Survey-of-Western-Australia/atratus) or via the email see links below.

If you have any questions about the tool you can contact the GDI team. You can [ask a question](mailto:gdi.contact@dmpe.wa.gov.au?subject=[Atratus%20Question]) or [flag an issue](mailto:gdi.contact@dmpe.wa.gov.au?subject=[Atratus%20Issue]), via these email links.


### Acknowledgements
This work would not be made possible without key contributions from members of the GDI team: Luke Smith, Tasman Gillfeather-Clark, and Jianli Zhi. 

Contributions to this project are welcome. Please refer to [contributing guide](#link) to learn more about how to contribute.
