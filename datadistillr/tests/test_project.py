"""
This file defines the class for testing the Project class.
"""
import json
import unittest
import responses
from responses import matchers
from datadistillr.datadistillr_account import DatadistillrAccount


class TestProject(unittest.TestCase):
    """
    This class is for testing the Project class.
    """
    BASE_URL = "https://app.datadistillr.io/api/"
    QUERY_BARRELS_ROUTE = BASE_URL + "queryBarrels"
    QUERY_RESULTS_ROUTE = BASE_URL + "queryResults"
    PROJECT_ROUTE = BASE_URL + "project"
    DATA_SOURCE_ROUTE = BASE_URL + "dataSource"

    # Real datadistillr account information, cannot be mocked because of authentication limitations
    MOCK_PROJECT_NAME = "Test Project 2"
    MOCK_PROJECT_TOKEN = 347151952
    MOCK_TAB_NAME = "months"
    MOCK_TAB_TOKEN = 298294315

    # Fake datadistillr account information
    MOCK_BARREL_TOKEN = 111111111
    MOCK_QUERY_TOKEN = 222222222
    MOCK_RUN_REQUEST_TOKEN = 333333333
    MOCK_DATASOURCE_TOKEN = 444444444
    MOCK_DATASOURCE_NAME = "data source"

    QUERY_RUN_ROUTE = QUERY_BARRELS_ROUTE + "/" + str(MOCK_BARREL_TOKEN) + "/query/" + \
        str(MOCK_QUERY_TOKEN) + "/run"

    QUERY_RESULTS_ROUTE = QUERY_RESULTS_ROUTE + "/" + str(MOCK_RUN_REQUEST_TOKEN)

    MOCK_QUERY_RUN_ROUTE_RESP = {
        'query': {'query': '--',
                  'token': MOCK_QUERY_TOKEN,
                  'queryBarrelToken': MOCK_BARREL_TOKEN},
        'requestToken': MOCK_RUN_REQUEST_TOKEN
    }

    MOCK_QUERY_RESULTS_ROUTE_RESP = {
        'results': [['1', 'January'], ['2', 'February'], ['3', 'March']],
        'summary': {'columnNames': ['Index', 'Month'], 'dataTypes': ['VARCHAR', 'VARCHAR'],
                    'rowsPerPage': 500, 'totalNumRows': 11, 'page': 1,
                    'totalPages': 1}, 'queryRun': {'app_id': 0, 'status': 'complete',
                                                   'token': MOCK_RUN_REQUEST_TOKEN,
                                                   'queryToken': MOCK_QUERY_TOKEN,
                                                   'numRows': 11}}

    def __init__(self, method_name: str) -> None:
        """
         The constructor for the TestProject class.

         Parameters:
             method_name (string): Test function to be run.
         """
        super().__init__(methodName=method_name)

        email = 'Amandaha29@gmail.com'
        password = 'Password1!'
        self.datadistillr_account = DatadistillrAccount(email, password)

        project_token = list(self.datadistillr_account.get_project_token_dict().keys())[0]
        self.project = self.datadistillr_account.get_project(project_token)

    @responses.activate
    def test_get_tab_token_dict(self):
        """
        Tests that get_tab_token_dict() returns dictionary of integers and strings.
        """

        tab_token_dict = self.project.get_tab_token_dict()
        tokens = tab_token_dict.keys()
        names = tab_token_dict.values()

        assert all(isinstance(token, int) for token in tokens)
        assert all(isinstance(name, str) for name in names)

    @responses.activate
    def test_get_tab_token(self):
        """
        Tests that get_tab_token() returns token matching tab name
        """

        # test get_tab_token() function
        tab_token = self.project.get_tab_token(self.MOCK_TAB_NAME)
        self.assertEqual(tab_token, self.MOCK_TAB_TOKEN)

    @responses.activate
    def test_execute_existing_query(self):
        """
        Tests that execute_existing_query() returns a dataframe.
        """

        mock_query_barrel_route_resp = {
            'queryBarrel': {
                'queries': [{'token': self.MOCK_QUERY_TOKEN,
                             'queryBarrelToken': self.MOCK_BARREL_TOKEN }],
                'token': self.MOCK_BARREL_TOKEN
            }
        }

        query_barrel_route = self.QUERY_BARRELS_ROUTE + "/" + str(self.MOCK_BARREL_TOKEN)

        # registering mock responses
        responses.add(
            method=responses.GET,
            url=query_barrel_route,
            json=mock_query_barrel_route_resp,
            status=200
        )
        responses.add(
            method=responses.GET,
            url=self.QUERY_RUN_ROUTE,
            json=self.MOCK_QUERY_RUN_ROUTE_RESP,
            status=200
        )
        responses.add(
            method=responses.GET,
            url=self.QUERY_RESULTS_ROUTE,
            json=self.MOCK_QUERY_RESULTS_ROUTE_RESP,
            status=200
        )

        # testing execute_existing_query function
        query_results_df = self.project.execute_existing_query(self.MOCK_BARREL_TOKEN)
        self.assertEqual(type(query_results_df).__name__, 'DataFrame')
        self.assertEqual(query_results_df['Index'].count(), 3)
        self.assertEqual(query_results_df['Month'].count(), 3)
        self.assertEqual(query_results_df.shape, (3, 2))

    @responses.activate
    def test_execute_new_query(self):
        """
        Tests that execute_new_query() returns a dataframe.
        """
        mock_query_barrel_name = "query barrel name"
        mock_query = "SQL QUERY"

        mock_new_query_barrel_route_resp = {
            'queryBarrel': {
                'name': mock_query_barrel_name,
                'queries': [
                    {'query': mock_query,
                     'token': self.MOCK_QUERY_TOKEN,
                     'queryBarrelToken': self.MOCK_BARREL_TOKEN}
                ],
                'query': mock_query,
                'token': self.MOCK_BARREL_TOKEN
            }
        }

        mock_new_query_barrel_details = {
            "projectSlug": self.MOCK_PROJECT_NAME.lower().replace(' ', '-'),
            "projectToken": self.MOCK_PROJECT_TOKEN,
            "name": mock_query_barrel_name,
            "active": True,
            "icon": "type-icon-file",
            "query": "  " + mock_query
        }

        # registering mock responses
        responses.add(
            method=responses.POST,
            url=self.QUERY_BARRELS_ROUTE,
            body=json.dumps(mock_new_query_barrel_route_resp, indent=2).encode('utf-8'),
            match=[matchers.json_params_matcher(mock_new_query_barrel_details)],
        )
        responses.add(
            method=responses.GET,
            url=self.QUERY_RUN_ROUTE,
            json=self.MOCK_QUERY_RUN_ROUTE_RESP,
            status=200
        )
        responses.add(
            method=responses.GET,
            url=self.QUERY_RESULTS_ROUTE,
            json=self.MOCK_QUERY_RESULTS_ROUTE_RESP,
            status=200
        )

        # testing execute_existing_query function
        query_results_df = self.project.execute_new_query(mock_query_barrel_name, mock_query)
        self.assertEqual(type(query_results_df).__name__, 'DataFrame')
        self.assertEqual(query_results_df['Index'].count(), 3)
        self.assertEqual(query_results_df['Month'].count(), 3)
        self.assertEqual(query_results_df.shape, (3, 2))

    @responses.activate
    def test_get_data_source_token_dict(self):
        """
        Tests that get_data_source_token_dict() returns dictionary with expected tokens and names
        """

        mock_data_sources_route_resp = {'dataSources': [{'name': self.MOCK_DATASOURCE_NAME,
                                                         'token': self.MOCK_DATASOURCE_TOKEN}]}

        data_source_route = self.PROJECT_ROUTE + "/" + str(self.MOCK_PROJECT_TOKEN) + "/dataSource"

        # register mock response
        responses.add(
            method=responses.GET,
            url=data_source_route,
            json=mock_data_sources_route_resp,
            status=200
        )

        # test get_data_source_token_dict() function
        data_source_token_dict = self.project.get_data_source_token_dict()
        data_source_tokens = list(data_source_token_dict.keys())
        data_source_names = list(data_source_token_dict.values())
        self.assertEqual(data_source_tokens, [self.MOCK_DATASOURCE_TOKEN])
        self.assertEqual(data_source_names, [self.MOCK_DATASOURCE_NAME])

    @responses.activate
    def test_get_data_source_token(self):
        """
        Tests that get_data_source_token() returns token matching data source name
        """

        mock_data_sources_route_resp = {'dataSources': [{'name': self.MOCK_DATASOURCE_NAME,
                                                         'token': self.MOCK_DATASOURCE_TOKEN}]}

        data_source_route = self.PROJECT_ROUTE + "/" + str(self.MOCK_PROJECT_TOKEN) + "/dataSource"

        # register mock response
        responses.add(
            method=responses.GET,
            url=data_source_route,
            json=mock_data_sources_route_resp,
            status=200
        )

        # test get_data_source_token() function
        data_source_token = self.project.get_data_source_token(self.MOCK_DATASOURCE_NAME)
        self.assertEqual(data_source_token, self.MOCK_DATASOURCE_TOKEN)

    @responses.activate
    def test_upload_files(self):
        """
        Tests that upload_files() uploads files successfully
        """

        mock_file_paths = ["datadistillr/tests/weekdays.csv", "datadistillr/tests/months.csv"]
        mock_files_to_upload = {'files': [{'name': 'weekdays.csv', 'size': 81, 'type': 'text/csv',
                                           'path': '/'},
                                          {'name': 'months.csv', 'size': 113, 'type': 'text/csv',
                                           'path': '/'}]
                                }

        mock_presigned_url1 = 'https://s3.amazonaws.com/prod.uploads.datadistillr.io/uploads' \
                              '/65b6fa8d/weekdays.csv?X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz' \
                              '-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA2BUAV67D6YOG3MHJ' \
                              '%2F20220502%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date' \
                              '=20220502T050421Z&X-Amz-SignedHeaders=host&X-Amz-Expires=30&X-Amz' \
                              '-Signature' \
                              '=b1de86d8c53e5ed23f4c204a15ce59992e19cffb7428c3c0503cb32bcc97b3d2 '

        mock_presigned_url2 = 'https://s3.amazonaws.com/prod.uploads.datadistillr.io/uploads' \
                              '/65b6fa8d/months.csv?X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz' \
                              '-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA2BUAV67D6YOG3MHJ' \
                              '%2F20220502%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date' \
                              '=20220502T050422Z&X-Amz-SignedHeaders=host&X-Amz-Expires=30&X-Amz' \
                              '-Signature' \
                              '=80b889d475b16d7b9bd7519dc7bbb61cfd09d2696b59742d487e4077cc7d76f0 '

        mock_upload_file_resp = {'presignedUrls': [mock_presigned_url1, mock_presigned_url2]}

        upload_file_route = self.DATA_SOURCE_ROUTE + "/" + str(self.MOCK_DATASOURCE_TOKEN) + "/file"

        # registering mock responses
        responses.add(
            method=responses.POST,
            url=upload_file_route,
            body=json.dumps(mock_upload_file_resp, indent=2).encode('utf-8'),
            match=[matchers.json_params_matcher(mock_files_to_upload)]
        )
        responses.add(
            method=responses.PUT,
            url=mock_presigned_url1,
            body="".encode('utf-8'),
            match=[matchers.header_matcher({'content-type': 'text/plain'})]
        )
        responses.add(
            method=responses.PUT,
            url=mock_presigned_url2,
            body="".encode('utf-8'),
            match=[matchers.header_matcher({'content-type': 'text/plain'})]
        )

        # test test_upload_files() function
        upload_file_resp = self.project.upload_files(self.MOCK_DATASOURCE_TOKEN, mock_file_paths)
        self.assertEqual(upload_file_resp, 'file uploaded successfully')
