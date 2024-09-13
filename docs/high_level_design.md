# High Level Design

This section covers where the geo digital toolkit sits in the overal domain specific ETL processing.

[NOTE THIS DOESN'T Render in Devops]
![A High level overview](.\assets\tchaikovsky.svg)

## Architecture
The geodigital toolkit is a 

The goal being that any SME can view the code and the data and see which files were included and why as well as which processing methods were applied. 

## An Example
Lets consider a simple example the consolidation of all petrophysical logging data from the data lake.

1. Connect to a Data Source (Data Lake/Local Copy)
2. Build the Astratus DataBase
    - Running the build command will create a sqlite database of all discovered data.
    - In addition to identifying all the data it also tags the files for SME defined tags.
3. Install and run a cygnet
    - A developed cygnet is designed to work natively with the Astratus database
    - Data that is fit for purpose for a given Cygnet will be identified by querying the astratus database.
    - These are the passed in and through the domain defined cleaning.
4. Enjoy your expert cleaned data.

---
## Tchaikovsky - Atratus - Cynget - GeoDigital

All systems we build in this space do so with a single goal.
Loading cleaned data to centralised 'cleaned' location.

Systems and Tools
 - Techaikovski : Orchestration, Loadbalancing, Resource Creation
 - Atratus : File Classification
 - Cygnet : Domain Specific Transformation and Load
 - Geo Digital Toolkit : Set of tools for loading to Geo Digital

Outputs
 - Geo Digital : Centralised Respository for all Data
 - Monitoring Dashboard : Centralised Dashboard for all Errors



## Futures
In future modules will be built to better characterise the curated data products produced by the cygnets for the characterisation of the Data for ML applications.

[Back to Summary](../readme.md)
***