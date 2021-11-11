import unittest
import requests
import datadistillr.datadistillr as ddr
from datadistillr.auth_exceptions import AuthorizationException
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ddr_api_test(unittest.TestCase):

    def test_failed_api_call(self):
        url = "https://devapp.datadistillr.io/v1/results/27921499"
        auth = "no_auth"
        try:
            ddr.datadistillr.get_dataframe(url, auth)
        except AuthorizationException as e:
            self.assertEqual(e.url, "https://devapp.datadistillr.io/v1/results/27921499")
            self.assertTrue((str(e.message).startswith("You are not authorized to access this resource.")))

    def test_successful_call(self):
        url = "https://devapp.datadistillr.io/v1/results/27921499"
        auth_token = "DDR1-HMAC-SHA256 Credential=ae63b76871914f18550704ebe2191dcd " \
                     "Signature=fc02eb28903474d21ad3c38ccd7a8bb519c3c9aebf6609ad5603d0ab09f0a31e "
        df = ddr.datadistillr.get_dataframe(url, auth_token)
        self.assertEqual(df['ip'].count(), 1000)
        self.assertEqual(df['datetime'].count(), 1000)
        self.assertEqual(df['duration'].count(), 1000)
        self.assertEqual(df.shape, (1000, 3))


if __name__ == '__main__':
    unittest.main()
