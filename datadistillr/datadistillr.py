import pandas as pd
import requests
from datadistillr import AuthorizationException


class datadistillr:

    @staticmethod
    def get_dataframe(url, api_key):
        '''
        DataDistillr allows you to publish your data by generating an API Endpoint.  To access your data, you will
        need an endpoint URL and an Authorization token. You can obtain both of these items in DataDistillr under the
        API Endpoints section.

        If the authorization is not successful this function throws an AuthorizationException.

        Full documentation is available here: https://docs.datadistillr.com/ddr/
        :param url:  Your dataset API URL
        :param api_key: Your unique dataset API key
        :return: A Pandas DataFrame of your data.
        '''
        headers = {"Authorization": api_key}
        response = requests.get(url, headers=headers, verify=False)

        # Case for unauthorized access
        if response.status_code == 401 or response.status_code == 403:
            raise AuthorizationException(url, "You are not authorized to access this resource.")
        # TODO Add more error response codes

        return pd.DataFrame(response.json()['results'], columns=response.json()['summary']['columnNames'])

