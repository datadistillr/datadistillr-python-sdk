# DataDistillr Python SDK

[![Total alerts](https://img.shields.io/lgtm/alerts/g/datadistillr/datadistillr-python-sdk.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/datadistillr/datadistillr-python-sdk/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/datadistillr/datadistillr-python-sdk.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/datadistillr/datadistillr-python-sdk/context:python)

This library allows you to programmatically interact with DataDistillr.  It is quite simple to programmatically pull data 
from DataDistillr for use in machine learning. 

### Methods
#### Datadistillr
* `get_dataframe(url, auth_token)`: Pulls your data and returns it in a Pandas DataFrame.
* `get_csv_from_api(url, auth_token, filename)`:  Pulls your data and returns it in a CSV file.
* `get_json_from_api(url, auth_token, filename)`:  Pulls your data and returns it in a JSON file.
* `get_parquet_from_api(url, auth_token, filename)`:  Pulls your data and returns it in a parquet file.
* `get_excel_from_api(url, auth_token, filename)`:  Pulls your data and returns it in an Excel file.
* `get_dict_from_api(url, auth_token, filename)`:  Pulls your data and returns it in a Python dictionary.

#### DatadistillrAccount
* `logout()`:  Logs you out of DataDistillr account.
* `get_projects()`:  Returns all projects in DataDistillr account as a list of Project objects.
* `get_project_token_dict()`: Returns dictionary with project tokens as keys and project names as values.
* `get_project(project_token)`:  Returns project object identified by project_token.
* `get_organizations()`:  Returns list organizations that DataDistillr account has access to.

#### Project
Note: A query barrel is represented by a tab in the DataDistillr user interface.
* `get_query_barrel_token_dict()`: Returns dictionary with query barrel tokens as keys and query barrel names as values.
* `execute_existing_query(barrel_token)`: Executes the most recent query in the query barrel identified by barrel_token.
* `execute_new_query(query_barrel_name, query)`: Creates new query barrel named query_barrel_name and executes query in new query barrel.
* `get_data_source_token_dict()`: Returns dictionary with data source tokens as keys and data source names as values. 
* `upload_files(data_source_token, file_paths)`: Uploads files to a data source. file_paths must be a list of absolute file path strings.


### Getting your Endpoint URL and Authorization Token
See https://docs.datadistillr.com/ddr/ for complete documentation on obtaining the URL and Auth Token.

### Usage 
Using the SDK in Python code is quite simple.  See the snippet below:
```python
import datadistillr.Datadistillr as ddr
url = <Your URL From DataDistillr>
auth_token = <AUTH TOKEN>
dataframe = ddr.datadistillr.get_dataframe(url, auth_token)
```