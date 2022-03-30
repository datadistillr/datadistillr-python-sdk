"""
This file is for testing the datadistillr API calls.
"""
import unittest
import requests
import datadistillr as ddr
requests.packages.urllib3.disable_warnings()


class DatadistillrApiTest(unittest.TestCase):
    """
    This class is for testing the datadistillr API calls.
    """

    def test_failed_api_call(self):
        """
        Tests that API call returns authorization error message if authorization token is incorrect.
        """

        url = "https://app.datadistillr.io/v1/results/27921499"
        auth = "no_auth"
        try:
            ddr.Datadistillr.get_dataframe(url, auth)
        except ddr.AuthorizationException as exception:
            self.assertEqual(exception.url, "https://app.datadistillr.io/v1/results/27921499")
            self.assertTrue((str(exception).startswith("You are not authorized to access "
                                                       "this resource.")))

    def test_successful_call(self):
        """
        Tests that API call returns expected values.
        """

        url = "https://app.datadistillr.io/v1/results/614364805"
        auth_token = "DDR1-HMAC-SHA256 Credential=b3880a85e304170f1b24ad8d3334845f " \
                     "Signature=f8c78f8b2e6b69ad79a44bfb441b2b6e06ec0b037184ecbd44cf45f2c82c78b6"
        data_frame = ddr.Datadistillr.get_dataframe(url, auth_token)
        self.assertEqual(data_frame['connection_client_host'].count(), 520)
        self.assertEqual(data_frame['city'].count(), 520)
        self.assertEqual(data_frame['country'].count(), 520)
        self.assertEqual(data_frame.shape, (520, 3))


if __name__ == '__main__':
    unittest.main()
