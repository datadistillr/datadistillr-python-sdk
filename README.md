# DataDistillr Python SDK

This library allows you to programmatically interact with DataDistillr.  It is quite simple to programmatically pull data 
from DataDistillr for use in machine learning. 

## Installing the SDK
The DataDistillr Python SDK is [available on Pypi](https://pypi.org/project/datadistillr/).  You can install it with pip as shown below:
```
pip install datadistillr
```

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
* `get_project_token(project_name)`: Returns project token that matches project_name
* `get_project(project_token)`:  Returns project object identified by project_token.
* `get_organizations()`:  Returns list organizations that DataDistillr account has access to.

#### Project
Note: A tab in the DataDistillr user interface is equivalent to a query barrel in API routes and responses. All public functions use the phrasing "tab" while all private functions use "query barrel"
* `get_tab_token_dict()`: Returns dictionary with tab tokens as keys and tab names as values.
* `get_tab_token(tab_name)`: Returns tab token that matches tab_name
* `execute_existing_query(tab_token)`: Executes the most recent query in the tab identified by tab_token.
* `execute_new_query(tab_name, query)`: Creates new tab named tab_name and executes query in new tab.
* `get_data_source_token_dict()`: Returns dictionary with data source tokens as keys and data source names as values.
* `get_data_source_token(data_source_name)`: Returns data source token that matches data_source_name
* `upload_files(data_source_token, file_paths)`: Uploads files to a data source. file_paths must be a list of absolute file path strings.


### Getting your Endpoint URL and Authorization Token
See https://docs.datadistillr.com/ddr/ for complete documentation on obtaining the URL and Auth Token.

### Usage 
Using the SDK in Python code is quite simple.  See the Examples below:

Importing SDK
```python
import datadistillr as ddr
```

Getting data from API Access Clients
```python
url = <Your URL From DataDistillr>
auth_token = <AUTH TOKEN>
dataframe = ddr.Datadistillr.get_dataframe(url, auth_token)
```


Logging in to a DataDistillr Account
```python
email = <Your Email linked to DataDistillr Account>
password = <Your Password>

ddr_account = ddr.DatadistillrAccount(email, password)
```

Getting a project object 
```python
project_name = <Name of project within DataDistillr Account>

project_token = ddr_account.get_project_token(project_name)
project = ddr_account.get_project(project_token)
```

Executing an existing query from a tab within a project
```python
tab_name = <Name of tab within project>

tab_token = project.get_tab_token(tab_name)
data_frame = project.execute_existing_query(tab_token)
```

Uploading files to a data source within a project
```python
data_source_name = <Name of data source within project>
file_paths = <List of absolute file path strings of files that you want to upload>

data_source_token = project.get_data_source_token(data_source_name)
project.upload_files(data_source_token, file_paths)
```
