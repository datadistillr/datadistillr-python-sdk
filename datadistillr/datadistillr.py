"""
This file defines the class for getting data from API Access Clients in Datadistillr account.
"""

import pandas as pd
import requests
from urllib3.exceptions import InsecureRequestWarning
from datadistillr.auth_exceptions import AuthorizationException


class Datadistillr:
    """
    This class is for getting data from API Access Clients in Datadistillr account.
    """

    @staticmethod
    def get_dataframe(url, api_key):
        """
        This function allows you to programmatically access data from DataDistillr and push it to a
        pandas DataFrame. DataDistillr allows you to publish your data by generating an API
        Endpoint. To access your data, you will need an endpoint URL and an Authorization token.
        You can obtain both of these items in DataDistillr under the API Endpoints section.

        If the authorization is not successful this function throws an AuthorizationException.

        Full documentation is available here: https://docs.datadistillr.com/ddr/
        :param url:  Your dataset API URL
        :param api_key: Your unique dataset API key
        :return: A Pandas DataFrame of your data.
        """
        response = Datadistillr.make_api_call(url, api_key)

        schema = response.json()['summary']['columnNames']
        data = response.json()['results']

        # Since we already retrieved the first page, decrement this by 1
        page_count = response.json()['summary']['totalPages'] - 1
        while page_count > 0:
            # Make next API call
            next_url = response.json()['summary']['nextPage']
            response = Datadistillr.make_api_call(next_url, api_key)

            # Append the data
            next_page = response.json()['results']
            data.extend(next_page)
            page_count -= page_count

        return pd.DataFrame(data, columns=schema)

    @staticmethod
    def make_api_call(url, api_key):
        """
        This function allows you to programmatically access data from DataDistillr.
        DataDistillr allows you to publish your data by generating an API Endpoint.
        To access your data, you will need an endpoint URL and an Authorization token. You can
        obtain both of these items in DataDistillr under the API Endpoints section.

        If the authorization is not successful this function throws an AuthorizationException.

        Full documentation is available here: https://docs.datadistillr.com/ddr/
        :param url:  Your dataset API URL
        :param api_key: Your unique dataset API key
        :return: response object from API call.
        """
        headers = {"Authorization": api_key}
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url, headers=headers, verify=False)

        # Case for unauthorized access
        if response.status_code in (401, 403):
            raise AuthorizationException(url, "You are not authorized to access this resource.")
        # TODO Add more error response codes

        return response


    @staticmethod
    def get_csv_from_api(url, api_key, filename):
        """
        This function allows you to programmatically access data from DataDistillr and push it to a
        CSV file.DataDistillr allows you to publish your data by generating an API Endpoint.
        To access your data, you will need an endpoint URL and an Authorization token. You can
        obtain both of these items in DataDistillr under the API Endpoints section.

        If the authorization is not successful this function throws an AuthorizationException.

        Full documentation is available here: https://docs.datadistillr.com/ddr/
        :param url:  Your dataset API URL
        :param api_key: Your unique dataset API key
        :param filename: The filename where you want your data written
        :return: A CSV file of your data.
        """
        data_frame = Datadistillr.get_dataframe(url, api_key)
        return data_frame.to_csv(filename)

    @staticmethod
    def get_json_from_api(url, api_key, filename):
        """
        This function allows you to programmatically access data from DataDistillr and push it to a
        JSON file. DataDistillr allows you to publish your data by generating an API Endpoint.
        To access your data, you will need an endpoint URL and an Authorization token. You can
        obtain both of these items in DataDistillr under the API Endpoints section.

        If the authorization is not successful this function throws an AuthorizationException.

        Full documentation is available here: https://docs.datadistillr.com/ddr/
        :param url:  Your dataset API URL
        :param api_key: Your unique dataset API key
        :param filename: The filename where you want your data written
        :return: A JSON file of your data.
        """
        data_frame = Datadistillr.get_dataframe(url, api_key)
        return data_frame.to_json(filename)

    @staticmethod
    def get_parquet_from_api(url, api_key, filename):
        """
        This function allows you to programmatically access data from DataDistillr and push it to a
        parquet file. DataDistillr allows you to publish your data by generating an API Endpoint.
        To access your data, you will need an endpoint URL and an Authorization token. You can
        obtain both of these items in DataDistillr under the API Endpoints section.

        If the authorization is not successful this function throws an AuthorizationException.

        Full documentation is available here: https://docs.datadistillr.com/ddr/
        :param url:  Your dataset API URL
        :param api_key: Your unique dataset API key
        :param filename: The filename where you want your data written
        :return: A parquet file of your data.
        """
        data_frame = Datadistillr.get_dataframe(url, api_key)
        return data_frame.to_parquet(filename)

    @staticmethod
    def get_excel_from_api(url, api_key, filename):
        """
        This function allows you to programmatically access data from DataDistillr and push it to an
        Excel file. DataDistillr allows you to publish your data by generating an API Endpoint.
        To access your data, you will need an endpoint URL and an Authorization token. You can
        obtain both of these items in DataDistillr under the API Endpoints section.

        If the authorization is not successful this function throws an AuthorizationException.

        Full documentation is available here: https://docs.datadistillr.com/ddr/
        :param url:  Your dataset API URL
        :param api_key: Your unique dataset API key
        :param filename: The filename where you want your data written
        :return: An Excel file of your data.
        """
        data_frame = Datadistillr.get_dataframe(url, api_key)
        return data_frame.to_excel(filename)

    @staticmethod
    def get_dict_from_api(url, api_key, filename):
        """
        This function allows you to programmatically access data from DataDistillr and push it to a
        Python dictionary. DataDistillr allows you to publish your data by generating an API
        Endpoint.  To access your data, you will need an endpoint URL and an Authorization token.
        You can obtain both of these items in DataDistillr under the API Endpoints section.

        If the authorization is not successful this function throws an AuthorizationException.

        Full documentation is available here: https://docs.datadistillr.com/ddr/
        :param url:  Your dataset API URL
        :param api_key: Your unique dataset API key
        :param filename: The filename where you want your data written
        :return: A Python dictionary file of your data.
        """
        data_frame = Datadistillr.get_dataframe(url, api_key)
        return data_frame.to_dict(filename)
