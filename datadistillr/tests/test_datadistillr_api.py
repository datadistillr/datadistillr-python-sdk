import unittest
import pandas as pd
import datadistillr.datadistillr as ddr
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from datadistillr.AuthorizationException import AuthorizationException

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ddr_api_test(unittest.TestCase):

    @staticmethod
    def test_failed_api_call(self):
        url = "https://devapp.datadistillr.io/v1/results/27921499"
        auth = "no_auth"
        self.assertRaises(AuthorizationException, ddr.get_dataframe(url, auth))


    def test_code(self):
        URL = "https://devapp.datadistillr.io/v1/results/27921499"

        AUTH_HEADER = "DDR1-HMAC-SHA256 Credential=ae63b76871914f18550704ebe2191dcd Signature=fc02eb28903474d21ad3c38ccd7a8bb519c3c9aebf6609ad5603d0ab09f0a31e"

        headers = {"Authorization": AUTH_HEADER}

        response = requests.get(URL, headers=headers, verify=False)
        data = pd.DataFrame(response.json()['results'], columns=response.json()['summary']['columnNames'])
        print(data.head())


if __name__ == '__main__':
    unittest.main()
