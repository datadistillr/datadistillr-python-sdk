# DataDistillr Python SDK

[![Total alerts](https://img.shields.io/lgtm/alerts/g/datadistillr/datadistillr-python-sdk.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/datadistillr/datadistillr-python-sdk/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/datadistillr/datadistillr-python-sdk.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/datadistillr/datadistillr-python-sdk/context:python)

This library allows you to programmatically interact with DataDistillr.  It is quite simple to programmatically pull data 
from DataDistillr for use in machine learning. 

## Methods
* `get_dataframe(url, auth_token)`: Pulls your data and returns it in a Pandas DataFrame.
* `get_csv_from_api(url, auth_token, filename)`:  Pulls your data and returns it in a CSV file.
* `get_json_from_api(url, auth_token, filename)`:  Pulls your data and returns it in a JSON file.
* `get_parquet_from_api(url, auth_token, filename)`:  Pulls your data and returns it in a parquet file.
* `get_excel_from_api(url, auth_token, filename)`:  Pulls your data and returns it in an Excel file.
* `get_dict_from_api(url, auth_token, filename)`:  Pulls your data and returns it in a Python dictionary.

### Getting your Endpoint URL and Authorization Token
See https://docs.datadistillr.com/ddr/ for complete documentation on obtaining the URL and Auth Token.

### Usage 
Using the SDK in Python code is quite simple.  See the snippet below:
```python
import datadistillr.datadistillr as ddr
url = <Your URL From DataDistillr>
auth_token = <AUTH TOKEN>
dataframe = ddr.datadistillr.get_dataframe(url, auth_token)
```