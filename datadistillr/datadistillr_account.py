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

    def __init__(self, email, password):
        """
        The constructor for Datadistillr class. Creates a session.

        Parameters:
            email (string): The email linked to Datadistillr account.
            password (string): The password linked to Datadistillr account.
        """

        requests.packages.urllib3.disable_warnings()
        # stores cookies, so you can make requests without multiple logins (pass around cookie)
        self.session = requests.Session()
        self.email = email
        self.password = password
        self.login_resp_json = self.login(self.email, self.password)
        self.is_logged_in = self.login_resp_json["loggedIn"]

    def login(self, email, password):
        """
        Login and authenticate to DataDistillr.

        Parameters:
            email (string): The email linked to account.
            password (string): The password linked to account.

        Returns:
            json: A json containing account details and login status.
        """

        user_info = {
            "email": email,
            "password": password,
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

    def get_projects(self):
        """
        Gets all projects in DataDistillr account.

        Returns:
            list<project>: A list of project objects
        """

        if not self.is_logged_in:
            raise Exception("login is incorrect")

        # URL to get project needs active org token, URL format may change
        org_token = self.login_resp_json["activeOrganization"]["token"]
        projects_page = self.BASE_URL + "organization/" + str(org_token) + "/projects"
        projects_response = self.session.get(url=projects_page, verify=False)

        # Converts response to JSON
        proj_resp_json = projects_response.json()

        # Gets the projects list
        proj_list = proj_resp_json["projects"]
        proj_object_list = []

        for proj in proj_list:
            # create new project object with json
            proj_object = Project(proj, self.session)
            proj_object_list.append(proj_object)

        return proj_object_list

    def get_project(self, project_name):
        """
        Gets an individual project object.

        Parameters:
            project_name (string): The name of a project in DataDistillr account.

        Returns:
            project: A project object. If project_name does not match existing projects, it returns
            "project not found".
        """

        if not self.is_logged_in:
            raise Exception("login is incorrect")

        proj_obj_list = self.get_projects()
        for proj_object in proj_obj_list:
            if proj_object.name == project_name:
                return proj_object
        return "project not found"

    def get_organizations(self):
        """
        Gets all organizations that the user has access to.

        Returns:
            list: A list of organizations that the user has access to.
        """

        if not self.is_logged_in:
            raise Exception("login is incorrect")

        organizations_response = self.session.get(url=self.ORGANIZATIONS_LIST, verify=False)
        organizations_resp_json = organizations_response.json()
        return organizations_resp_json["organizations"]
