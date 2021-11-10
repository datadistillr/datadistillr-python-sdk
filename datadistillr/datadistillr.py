import pandas as pd
import requests
from . import AuthorizationException


class datadistillr:

    @classmethod
    def get_dataframe(cls, url, api_key):
        headers = {"Authorization": api_key}
        response = requests.get(url, headers=headers, verify=False)

        # Case for unauthorized access
        if response.status_code == 401:
            raise AuthorizationException(url, "You are not authorized to access this resource.")

        URL = "https://devapp.datadistillr.io/v1/results/27921499"

        AUTH_HEADER = "DDR1-HMAC-SHA256 Credential=ae63b76871914f18550704ebe2191dcd Signature=fc02eb28903474d21ad3c38ccd7a8bb519c3c9aebf6609ad5603d0ab09f0a31e"

        headers = {"Authorization": AUTH_HEADER}

        response = requests.get(URL, headers=headers, verify=False)
        return pd.DataFrame(response.json()['results'], columns=response.json()['summary']['columnNames'])
