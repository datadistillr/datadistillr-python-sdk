"""
This file defines the project class for getting project level data.
"""


class Project:
    """
    This is a class for getting project level data.

    Attributes:
        proj_details (json): json containing details of project.
    """

    def __init__(self, proj_details, _curr_session):
        """
        The constructor for Datadistillr class. Creates a session.

        Parameters:
            proj_details (json): json containing details of project.
        """

        self.session = _curr_session
        self.details_json = proj_details
        self.name = self.details_json["name"]
        self.project_token = self.details_json["token"]

    def get_project_barrel_token(self, tab_name):
        """
        Gets barrel token associated with tab within project.

        Parameters:
            tab_name (string): name of tab in project.

        Returns:
            int: barrel token associated with tab.
        """
        # added function to pass pylint
        print(tab_name)
        return self.details_json

    def get_tab(self, tab_name):
        """
        Gets results of active query in tab.

        Parameters:
            tab_name (string): name of query in project.

        Returns:
            pandas dataframe: results from active query.
        """
        # added function to pass pylint
        print(tab_name)
        return self.details_json
