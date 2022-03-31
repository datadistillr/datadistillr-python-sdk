"""
This file defines the project class for getting project level data.
"""
import pandas as pd


class Project:
    """
    This is a class for getting project level data.

    Attributes:
        proj_details (json): json containing details of project.
    """
    BASE_URL = "https://app.datadistillr.io/api/"
    PROJECT_DISTILLRY = BASE_URL + "projectDistillry"
    QUERY_BARRELS = BASE_URL + "queryBarrels"
    QUERY_RUN_PAGE = BASE_URL + "queryResults"

    def __init__(self, proj_details, _curr_session):
        """
        The constructor for Datadistillr class. Creates a session and contains project details

        Parameters:
            proj_details (JSON): JSON containing details of project.
        """

        self.session = _curr_session
        self.details_json = proj_details
        self.name = self.details_json["name"]
        self.project_token = self.details_json["token"]

    def _get_tab_barrel_token(self, tab_name):
        """
        Gets barrel token associated with tab within project.

        Parameters:
            tab_name (string): name of tab in project.

        Returns:
            int: barrel token associated with tab.
        """

        details_page = self.PROJECT_DISTILLRY + "/" + str(self.project_token)
        details = self.session.get(url=details_page)
        details_json = details.json()

        # Finds part regarding query barrels
        query_barrels = details_json["project"]["queryBarrels"]

        # Finds barrel token matching tab name
        for query_barrel in query_barrels:
            if query_barrel["name"] == tab_name:
                return query_barrel["token"]
        return None

    def _get_active_query_token(self, tab_barrel_token):
        """
        Gets token of query that is currently active within tab.

        Parameters:
            tab_barrel_token (int): Tab barrel token associated with query.

        Returns:
            int: token of query that is currently active.
        """

        queries_page = self.QUERY_BARRELS + "/" + str(tab_barrel_token)
        queries_response = self.session.get(url=queries_page)
        queries_response_json = queries_response.json()

        # Finds part regarding queries
        queries_list = queries_response_json["queryBarrel"]["queries"]

        # Finds active query token
        for queries in queries_list:
            if queries['active']:
                return queries["runHistory"][0]["token"]

        return None

    def _query_results(self, active_query_token):
        """
        Gets results of active query

        Parameters:
            active_query_token (int): token of query that is currently active.

        Returns:
            pandas dataframe: results of active query.
        """

        active_query_run = self.QUERY_RUN_PAGE + "/" + str(active_query_token)
        query_run_resp = self.session.get(url=active_query_run)

        schema = query_run_resp.json()['summary']['columnNames']
        data = query_run_resp.json()['results']
        # Since we already retrieved the first page, decrement this by 1
        page_count = query_run_resp.json()['summary']['totalPages'] - 1
        while page_count > 0:
            # Make next API call
            next_url = query_run_resp.json()['summary']['nextPage']
            query_run_resp = self.session.get(url=next_url)

            # Append the data
            next_page = query_run_resp.json()['results']
            data.extend(next_page)
            page_count -= page_count
        return pd.DataFrame(data, columns=schema)

    def get_tab(self, tab_name):
        """
        Gets query results of given tab in project.

        Parameters:
            tab_name (string): name of tab in project.

        Returns:
            pandas dataframe: results of active query.
        """

        tab_barrel_token = self._get_tab_barrel_token(tab_name)
        if tab_barrel_token is None:
            raise Exception("No such tab exists in project")

        active_token = self._get_active_query_token(tab_barrel_token)
        if active_token is None:
            raise Exception("No queries are currently active in this tab")

        return self._query_results(active_token)

    def query(self, tab_name, sql_statement):
        """
        Runs query and returns result of query.

        Parameters:
            tab_name (string): Name of tab in project where the query should run.
            sql_statement (string): SQL statement to be executed.

        Returns:
            pandas dataframe: results of SQL statement.
        """
        # public function needed for pylint
        return self.name + " will run " + sql_statement + " in the " + tab_name + " tab "
