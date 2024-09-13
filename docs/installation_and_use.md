<p style="text-align: center;font-size:2em"> Git Submodules </p>

---
In the future our team will produce many cygnets. These cygnets handle the extraction and transformation of domain specific ETL processes. Due to the nature of our organisation many domain experts will only want to utilise individual ETL processes.

As such our design starts by making these processes function independantly. 

The overall goal being that correctly classified files are ingested into their corresponding tables to facilitate easy analytics. 

---

## Tchiakovski
A yet to be implemented project that will handle orchestration of the various cygnets. Taking a categorised file as an input, which is parsed into the appropriate cygnet. Into the orchestration code the various cygnets will be installed as submodles and loaded.

---

## Full List of Cygnet Projects
- Skippy - Downhole Geophysical Logging las data harmonisation.

[Back to Summary](../readme.md)