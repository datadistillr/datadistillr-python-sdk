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

        url = "https://app.datadistillr.io/v1/results/298294315"
        auth = "no_auth"
        try:
            ddr.Datadistillr.get_dataframe(url, auth)
        except ddr.AuthorizationException as exception:
            self.assertEqual(exception.url, url)
            self.assertIn("You are not authorized to access this resource", str(exception))

    def test_successful_call(self):
        """
        Tests that API call returns expected values.
        """

        url = "https://app.datadistillr.io/v1/results/298294315"
        auth_token = "DDR1-HMAC-SHA256 Credential=cb161e29b3baf02c26a25b2809ebb1e3 " \
                     "Signature=19488068ba57273290a924896662fdfa50f89b7e0b8558e165d94e4582f3c082"
        data_frame = ddr.Datadistillr.get_dataframe(url, auth_token)
        self.assertEqual(data_frame['col_1'].count(), 11)
        self.assertEqual(data_frame['January'].count(), 11)
        self.assertEqual(data_frame.shape, (11, 2))


if __name__ == '__main__':
    unittest.main()
