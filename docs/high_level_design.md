# High Level Design

This section covers where the geo digital toolkit sits in the overal domain specific ETL processing.

[NOTE THIS DOESN'T Render in Devops]
![A High level overview](.\assets\tchaikovsky.svg)

## Architecture
The geodigitaltoolkit is intended to have 3 core modules.
 - database
    - intended to handle any flavour of sql operations.
 - utils
    - intended to handle internally known exceptions.
    - logging operations
 - storage *
    - a future extension that will handles connections and file handling operations
    - moving files, blob storage, file streams etc

---
## Tchaikovsky - Atratus - Cynget - GeoDigital

All systems we build in this space do so with a single goal.
Loading cleaned data to centralised 'cleaned' location.

Systems and Tools
 - Techaikovski : Orchestration, Loadbalancing, Resource Creation
 - Atratus : File Classification (Cateloguing?)
 - Cygnet : Domain Specific Transformation and Load
 - Geo Digital Toolkit : Set of tools for loading to Geo Digital and logging

Outputs
 - Geo Digital : Centralised Respository for all Data
 - Monitoring Dashboard : Centralised Dashboard for all Errors

## Futures
In future modules will be built to better characterise the curated data products produced by the cygnets for the characterisation of the Data for ML applications.

[Back to Summary](../readme.md)
***