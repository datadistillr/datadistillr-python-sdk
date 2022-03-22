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
        url = "https://app.datadistillr.io/v1/results/614364805"
        auth_token = "DDR1-HMAC-SHA256 Credential=b3880a85e304170f1b24ad8d3334845f " \
                     "Signature=f8c78f8b2e6b69ad79a44bfb441b2b6e06ec0b037184ecbd44cf45f2c82c78b6"
        df = ddr.datadistillr.get_dataframe(url, auth_token)
        self.assertEqual(df['connection_client_host'].count(), 520)
        self.assertEqual(df['city'].count(), 520)
        self.assertEqual(df['country'].count(), 520)
        self.assertEqual(df.shape, (520, 3))


if __name__ == '__main__':
    unittest.main()
