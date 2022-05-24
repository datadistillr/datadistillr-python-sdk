"""
This file defines the class for getting account level data from Datadistillr account.
"""

import requests
from datadistillr.project import Project


class DatadistillrAccount:
    """
    This is a class for getting account level data from Datadistillr account.

    Attributes:
        email (string): The email linked to Datadistillr account.
        password (string): The password linked to Datadistillr account.
    """

    BASE_URL = "https://app.datadistillr.io/api/"
    LOGIN_PAGE = BASE_URL + "login"
    ORGANIZATIONS_LIST = BASE_URL + "organization"
    LOGOUT_PAGE = BASE_URL + 'logout'
    PROJECT_DISTILLRY = BASE_URL + "projectDistillry"

    def __init__(self, email, password):
        """
        The constructor for the DatadistillrAccount class. Creates a session.

        Parameters:
            email (string): The email linked to Datadistillr account.
            password (string): The password linked to Datadistillr account.
        """
        requests.packages.urllib3.disable_warnings()
        # stores cookies, so you can make requests without multiple logins (pass around cookie)
        self.session = requests.Session()
        self.email = email
        self.password = password
        self.login_resp_json = self._login()
        self.is_logged_in = self.login_resp_json["loggedIn"]
        self.proj_token_dict = {}

    def _login(self):
        """
        Login and authenticate to DataDistillr.

        Returns:
            json: A json containing account details and login status.
        """

        user_info = {
            "email": self.email,
            "password": self.password,
            "invitations": {
                "organizationInvitationToken": None,
                "projectInvitationToken": None,
                "teamInvitationToken": None}
        }
        login_response = self.session.post(url=self.LOGIN_PAGE, json=user_info, verify=False)
        login_resp_json = login_response.json()
        return login_resp_json

    def logout(self):
        """
        Log user out of DataDistillr account.

        Returns:
            json: A json containing account details and login status.
        """

        logout_response = self.session.get(url=self.LOGOUT_PAGE, verify=False)
        logout_resp_json = logout_response.json()
        self.is_logged_in = logout_resp_json["loggedIn"]
        return logout_resp_json

    def get_project_token_dict(self):
        """
        Returns dictionary with project tokens as keys and project names as values.

        Returns:
            dictionary (int -> str): dictionary with project token as key and project name as value.
        """

        # check if login is correct
        if not self.is_logged_in:
            raise Exception("login is incorrect")

        org_token = self.login_resp_json["activeOrganization"]["token"]
        projects_page = self.BASE_URL + "organization/" + str(org_token) + "/projects"
        projects_response = self.session.get(url=projects_page, verify=False)

        # Converts response to JSON
        proj_resp_json = projects_response.json()

        # Gets the projects list
        proj_list = proj_resp_json["projects"]

        for proj in proj_list:
            # Creates a dictionary of all projects and their tokens
            self.proj_token_dict[proj["token"]] = proj["name"]
        return self.proj_token_dict

    def get_project_token(self, project_name):
        """
        Returns project token that matches project_name

        Returns:
            int: project token
        """

        proj_token_dict = self.get_project_token_dict()
        for token, name in proj_token_dict.items():
            if project_name == name:
                return token
        raise Exception("token not found")

    def get_project(self, project_token):
        """
        Returns individual project object.

        Parameters:
            project_token (int): Token that uniquely identifies project. A dictionary with all
            project tokens can be found using the get_project_token_dict() function.

        Returns:
            project: A project object.
        """

        # check if login is correct
        if not self.is_logged_in:
            return "login is incorrect"

        project_details_page = self.PROJECT_DISTILLRY + "/" + str(project_token)
        # Gets the url
        project_details = self.session.get(url=project_details_page)
        # Parses the response from JSON to a python dictionary
        project_details_json = project_details.json()['project']
        proj_object = Project(project_details_json, self.session)
        # Returns the parsed JSON
        return proj_object

    def get_projects(self):
        """
        Returns all projects in DataDistillr account.

        Returns:
            list<Project>: A list of project objects.
        """

        if not self.is_logged_in:
            raise Exception("login is incorrect")

        proj_object_list = []

        project_tokens = self.get_project_token_dict().keys()
        for project_token in project_tokens:
            proj_object = self.get_project(project_token)
            proj_object_list.append(proj_object)

        return proj_object_list

    def get_organizations(self):
        """
        Returns all organizations that the user has access to.

        Returns:
            list: A list of organizations that the user has access to.
        """

        if not self.is_logged_in:
            raise Exception("login is incorrect")

        organizations_response = self.session.get(url=self.ORGANIZATIONS_LIST, verify=False)
        organizations_resp_json = organizations_response.json()
        return organizations_resp_json["organizations"]
