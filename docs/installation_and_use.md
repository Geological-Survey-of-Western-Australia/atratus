<p style="text-align: center;font-size:2em"> Git Submodules </p>

---
Due to the nature of our organisation many domain experts will only want to utilise individual ETL processes. As such our design starts by making these processes function independantly. The most effective approach for this (short of publishing the code to a public repo - far future), is to utilise gits submodule functionality. 

```
git submodule add <devops-url>
```

For projects that will use the geo digital toolkit, they should be installed in the root-directory of new project eg. This facilitates the named based imports from the submodule

```
├── repo_folder
│   ├── gdi_geodigital
│   │   ├── database
│   │   ├── utils
│   ├── gdi_new_project
│   │   ├── model
│   ├── my_test_notebook.ipynb

```

This allows for full name imports from the geo-digital-toolkit as below.

```python 
from gdi_geodigital import geo_digital_tools as gdt
```
---

[Back to Summary](../readme.md)