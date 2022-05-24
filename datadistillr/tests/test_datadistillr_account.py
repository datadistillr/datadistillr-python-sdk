"""
This file defines the class for testing the DatadistillrAccount class.
"""

import unittest
import responses
from datadistillr.datadistillr_account import DatadistillrAccount
from datadistillr.project import Project


class TestDatadistillrAccount(unittest.TestCase):
    """
    This class is for testing the DatadistillrAccount class.
    """

    BASE_URL = "https://app.datadistillr.io/api/"
    ORGANIZATIONS_ROUTE = BASE_URL + "organization"
    PROJECT_DISTILLRY_ROUTE = BASE_URL + "projectDistillry"
    # Real datadistillr account information, cannot be mocked because of authentication limitations
    MOCK_ORG_TOKEN = 880610291

    # Fake datadistillr account information
    MOCK_PROJ1_NAME = "Project 1"
    MOCK_PROJ1_TOKEN = 111111111
    MOCK_PROJ2_NAME = "Project 2"
    MOCK_PROJ2_TOKEN = 222222222

    MOCK_PROJ1_ROUTE_RESP = {'project': {'name': MOCK_PROJ1_NAME, 'token': MOCK_PROJ1_TOKEN}}
    MOCK_PROJ2_ROUTE_RESP = {'project': {'name': MOCK_PROJ2_NAME, 'token': MOCK_PROJ2_TOKEN}}
    MOCK_PROJS_ROUTE_RESP = {'projects': [MOCK_PROJ1_ROUTE_RESP['project'],
                                          MOCK_PROJ2_ROUTE_RESP['project']]}
    MOCK_ORGS_ROUTE_RESP = {'organizations': [{'name': 'hidden', 'token': 880610291}]}

    def __init__(self, method_name: str) -> None:
        """
         The constructor for the TestDatadistillrAccount class.

         Parameters:
             method_name (string): Test function to be run.
         """
        super().__init__(methodName=method_name)

        # init DatadistillrAccount object
        email = 'Amandaha29@gmail.com'
        password = 'Password1!'
        self.datadistillr_account = DatadistillrAccount(email, password)

    def test_login(self):
        """
        Tests that DataDistillrAccount is authenticated once initialized.
        """

        self.assertTrue(self.datadistillr_account.is_logged_in)

    def test_logout(self):
        """
        Tests that DataDistillrAccount cannot access functions if logged out.
        """

        self.datadistillr_account.logout()
        self.assertFalse(self.datadistillr_account.is_logged_in)
        self.assertRaises(Exception, self.datadistillr_account.get_projects)
        self.assertRaises(Exception, self.datadistillr_account.get_project_token_dict)
        self.assertRaises(Exception, self.datadistillr_account.get_project)
        self.assertRaises(Exception, self.datadistillr_account.get_organizations)

    @responses.activate
    def test_get_projects(self):
        """
        Tests that get_projects() returns list of Project objects with expected names.
        """

        projs_route = self.BASE_URL + "organization/" + str(self.MOCK_ORG_TOKEN) + "/projects"
        proj1_route = self.PROJECT_DISTILLRY_ROUTE + "/" + str(self.MOCK_PROJ1_TOKEN)
        proj2_route = self.PROJECT_DISTILLRY_ROUTE + "/" + str(self.MOCK_PROJ2_TOKEN)

        # register mock response
        responses.add(responses.GET, projs_route, json=self.MOCK_PROJS_ROUTE_RESP, status=200)
        responses.add(responses.GET, proj1_route, json=self.MOCK_PROJ1_ROUTE_RESP, status=200)
        responses.add(responses.GET, proj2_route, json=self.MOCK_PROJ2_ROUTE_RESP, status=200)

        # test get_projects() function
        projects = self.datadistillr_account.get_projects()
        assert all(isinstance(proj, Project) for proj in projects)
        self.assertEqual(projects[0].name, self.MOCK_PROJ1_NAME)
        self.assertEqual(projects[1].name, self.MOCK_PROJ2_NAME)

    @responses.activate
    def test_get_project_token_dict(self):
        """
        Tests that get_project_token_dict() returns dictionary with expected tokens and names
        """

        projs_route = self.BASE_URL + "organization/" + str(self.MOCK_ORG_TOKEN) + "/projects"

        # register mock response
        responses.add(responses.GET, projs_route, json=self.MOCK_PROJS_ROUTE_RESP, status=200)

        # test get_project_token_dict() function
        project_token_dict = self.datadistillr_account.get_project_token_dict()
        project_tokens = list(project_token_dict.keys())
        project_names = list(project_token_dict.values())
        self.assertEqual(project_tokens, [self.MOCK_PROJ1_TOKEN, self.MOCK_PROJ2_TOKEN])
        self.assertEqual(project_names, [self.MOCK_PROJ1_NAME, self.MOCK_PROJ2_NAME])

    @responses.activate
    def test_get_project_token(self):
        """
        Tests that get_project_token() returns token matching project name
        """

        projs_route = self.BASE_URL + "organization/" + str(self.MOCK_ORG_TOKEN) + "/projects"

        # register mock response
        responses.add(responses.GET, projs_route, json=self.MOCK_PROJS_ROUTE_RESP, status=200)

        # test get_project_token() function
        project_token = self.datadistillr_account.get_project_token(self.MOCK_PROJ1_NAME)
        self.assertEqual(project_token, self.MOCK_PROJ1_TOKEN)

    @responses.activate
    def test_get_project(self):
        """
        Tests that get_project() returns a project object with expected name.
        """

        proj1_route = self.PROJECT_DISTILLRY_ROUTE + "/" + str(self.MOCK_PROJ1_TOKEN)

        # register mock response
        responses.add(responses.GET, proj1_route, json=self.MOCK_PROJ1_ROUTE_RESP, status=200)

        # test get_project() function
        project = self.datadistillr_account.get_project(self.MOCK_PROJ1_TOKEN)
        self.assertIsInstance(project, Project)
        self.assertEqual(project.name, self.MOCK_PROJ1_NAME)

    @responses.activate
    def test_get_organizations(self):
        """
        Tests that get_organizations() returns a list of organization dictionaries.
        """

        # register mock response
        responses.add(responses.GET, self.ORGANIZATIONS_ROUTE, json=self.MOCK_ORGS_ROUTE_RESP,
                      status=200)

        # test get_organizations() function
        organizations = self.datadistillr_account.get_organizations()
        self.assertEqual(organizations, self.MOCK_ORGS_ROUTE_RESP['organizations'])
