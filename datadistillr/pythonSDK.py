import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datadistillr.project import project

class datadistillr:
    base_url = "https://app.datadistillr.io/api/"
    login_page = base_url + "login"
    organizations_list = organizations = base_url + "organization"
    logout_page = base_url + 'logout'

    def __init__(self, email, password):
        """Creates session"""
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        # stores cookies, so you can make requests without multiple logins (pass around cookie)
        self.session = requests.Session()
        self.email = email
        self.password = password
        self.login_resp_json = self.login()
        self.is_logged_in = self.login_resp_json["loggedIn"]
        pass

    def login(self):
        """Takes in email and password, converts to dictionary, then converts to JSON, and posts the user info to the login page"""
        print("logging in ...")
        user_info = {
            "email": self.email,
            "password": self.password,
            "invitations": {
                "organizationInvitationToken": None,
                "projectInvitationToken": None,
                "teamInvitationToken": None}
        }

        login_response = self.session.post(url=self.login_page, json=user_info, verify=False)
        login_resp_json = login_response.json()
        return login_resp_json

    def logout(self):
        """Logout user out of DataDistillr platform page"""
        logout_response = self.session.get(url=self.logout_page, verify=False)
        logout_resp_json = logout_response.json()
        self.is_logged_in = logout_resp_json["loggedIn"]
        return logout_resp_json

    # Returns a list of project objects to which the user has access.
    def get_projects(self):
        """Gets projects page"""
        # check if login is correct
        if not self.is_logged_in:
            return "login is incorrect"

        # URL to get project needs active org token, URL format may change
        org_token = self.login_resp_json["activeOrganization"]["token"]
        projects_page = self.base_url + "organization/" + str(org_token) + "/projects"
        projects_response = self.session.get(url=projects_page, verify=False)

        # Converts response to JSON
        proj_resp_json = projects_response.json()

        # Gets the projects list
        proj_list = proj_resp_json["projects"]
        proj_object_list = []

        for i in range(len(proj_list)):
            # create new project object with json
            proj_object = project(proj_list[i], self.session)
            proj_object_list.append(proj_object)

        # Returns list of the project object
        return proj_object_list

    # Retrieves an individual project object
    def get_project(self, project_name):
        # check if login is correct
        if not self.is_logged_in:
            return "login is incorrect"

        proj_list = self.get_projects()
        for i in range(len(proj_list)):
            proj_object = proj_list[i]
            if proj_object.name == project_name:
                return proj_object
        return "project not found"

    # Returns a list of organizations the user has access.
    def get_organizations(self):
        # check if login is correct
        if not self.is_logged_in:
            return "login is incorrect"
        organizations_response = self.session.get(url=self.organizations_list, verify=False)
        organizations_resp_json = organizations_response.json()
        return organizations_resp_json["organizations"]
