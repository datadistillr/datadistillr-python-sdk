import pandas as pd
import requests
from datadistillr import AuthorizationException
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class datadistillr:

    @staticmethod
    def get_dataframe(url, api_key):
        '''
        This function allows you to programmatically access data from DataDistillr and push it to a pandas DataFrame.
        DataDistillr allows you to publish your data by generating an API Endpoint.  To access your data, you will
        need an endpoint URL and an Authorization token. You can obtain both of these items in DataDistillr under the
        API Endpoints section.

        If the authorization is not successful this function throws an AuthorizationException.

        Full documentation is available here: https://docs.datadistillr.com/ddr/
        :param url:  Your dataset API URL
        :param api_key: Your unique dataset API key
        :return: A Pandas DataFrame of your data.
        '''
        response = datadistillr.make_api_call(url, api_key)

        schema = response.json()['summary']['columnNames']
        data = response.json()['results']

        # Since we already retrieved the first page, decrement this by 1
        pageCount = response.json()['summary']['totalPages'] - 1
        while pageCount > 0:
            # Make next API call
            nextUrl = response.json()['summary']['nextPage']
            response = datadistillr.make_api_call(nextUrl, api_key)

            #Append the data
            next_page = response.json()['results']
            data.extend(next_page)
            pageCount -= pageCount

        return pd.DataFrame(data, columns=schema)

    @staticmethod
    def make_api_call(url, api_key):
        headers = {"Authorization": api_key}
        if "devapp.datadistillr" in url:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.get(url, headers=headers, verify=False)
        else:
            response = requests.get(url, headers=headers)

        # Case for unauthorized access
        if response.status_code == 401 or response.status_code == 403:
            raise AuthorizationException(url, "You are not authorized to access this resource.")
        # TODO Add more error response codes

        return response


    @staticmethod
    def get_csv_from_api(url, api_key, filename):
        '''
        This function allows you to programmatically access data from DataDistillr and push it to a CSV file.
        DataDistillr allows you to publish your data by generating an API Endpoint.  To access your data, you will
        need an endpoint URL and an Authorization token. You can obtain both of these items in DataDistillr under the
        API Endpoints section.

        If the authorization is not successful this function throws an AuthorizationException.

        Full documentation is available here: https://docs.datadistillr.com/ddr/
        :param url:  Your dataset API URL
        :param api_key: Your unique dataset API key
        :param filename: The filename where you want your data written
        :return: A CSV file of your data.
        '''
        df = datadistillr.get_dataframe(url, api_key)
        return df.to_csv(filename)

    @staticmethod
    def get_json_from_api(url, api_key, filename):
        '''
        This function allows you to programmatically access data from DataDistillr and push it to a JSON file.
        DataDistillr allows you to publish your data by generating an API Endpoint.  To access your data, you will
        need an endpoint URL and an Authorization token. You can obtain both of these items in DataDistillr under the
        API Endpoints section.

        If the authorization is not successful this function throws an AuthorizationException.

        Full documentation is available here: https://docs.datadistillr.com/ddr/
        :param url:  Your dataset API URL
        :param api_key: Your unique dataset API key
        :param filename: The filename where you want your data written
        :return: A JSON file of your data.
        '''
        df = datadistillr.get_dataframe(url, api_key)
        return df.to_json(filename)

    @staticmethod
    def get_parquet_from_api(url, api_key, filename):
        '''
        This function allows you to programmatically access data from DataDistillr and push it to a parquet file.
        DataDistillr allows you to publish your data by generating an API Endpoint.  To access your data, you will
        need an endpoint URL and an Authorization token. You can obtain both of these items in DataDistillr under the
        API Endpoints section.

        If the authorization is not successful this function throws an AuthorizationException.

        Full documentation is available here: https://docs.datadistillr.com/ddr/
        :param url:  Your dataset API URL
        :param api_key: Your unique dataset API key
        :param filename: The filename where you want your data written
        :return: A parquet file of your data.
        '''
        df = datadistillr.get_dataframe(url, api_key)
        return df.to_parquet(filename)

    @staticmethod
    def get_excel_from_api(url, api_key, filename):
        '''
        This function allows you to programmatically access data from DataDistillr and push it to an Excel file.
        DataDistillr allows you to publish your data by generating an API Endpoint.  To access your data, you will
        need an endpoint URL and an Authorization token. You can obtain both of these items in DataDistillr under the
        API Endpoints section.

        If the authorization is not successful this function throws an AuthorizationException.

        Full documentation is available here: https://docs.datadistillr.com/ddr/
        :param url:  Your dataset API URL
        :param api_key: Your unique dataset API key
        :param filename: The filename where you want your data written
        :return: An Excel file of your data.
        '''
        df = datadistillr.get_dataframe(url, api_key)
        return df.to_excel(filename)

    @staticmethod
    def get_dict_from_api(url, api_key, filename):
        '''
        This function allows you to programmatically access data from DataDistillr and push it to a Python dictionary.
        DataDistillr allows you to publish your data by generating an API Endpoint.  To access your data, you will
        need an endpoint URL and an Authorization token. You can obtain both of these items in DataDistillr under the
        API Endpoints section.

        If the authorization is not successful this function throws an AuthorizationException.

        Full documentation is available here: https://docs.datadistillr.com/ddr/
        :param url:  Your dataset API URL
        :param api_key: Your unique dataset API key
        :param filename: The filename where you want your data written
        :return: A Python dictionary file of your data.
        '''
        df = datadistillr.get_dataframe(url, api_key)
        return df.to_dict(filename)
