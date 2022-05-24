"""
This file defines the project class for getting project level data.
"""
import time
import os
import ntpath
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
    PROJECT_PAGE = BASE_URL + "project"
    DATA_SOURCE_PAGE = BASE_URL + "dataSource"
    MAX_ATTEMPTS = 20
    SLEEP_TIMER = 5.0

    def __init__(self, proj_details, _curr_session):
        """
        The constructor for Datadistillr class. Creates a session and contains project details.

        Parameters:
            proj_details (JSON): JSON containing details of project.
        """

        self.session = _curr_session
        self.details_json = proj_details
        self.name = self.details_json["name"]
        self.project_token = self.details_json["token"]
        self.barrel_token_dict = {}
        self.data_source_token_dict = {}

    def get_tab_token_dict(self):
        """
        Returns dictionary with tab tokens as keys and tab names as values.
        A tab in the DataDistillr user interface is equivalent to a query barrel in API routes and
        responses.

        Returns:
            dictionary (int -> str): dictionary with query barrel token as key and query barrel
            name as value.
        """

        project_query_barrels = self.details_json["queryBarrels"]
        for query_barrel in project_query_barrels:
            self.barrel_token_dict[query_barrel["token"]] = query_barrel["name"]
        return self.barrel_token_dict

    def get_tab_token(self, tab_name):
        """
        Returns tab token that matches tab_name

        Returns:
            int: tab token
        """

        tab_token_dict = self.get_tab_token_dict()
        for token, name in tab_token_dict.items():
            if tab_name == name:
                return token
        raise Exception("token not found")

    def _get_recent_query_token(self, barrel_token):
        """
        Returns token of most recent query in query barrel.
        A tab in the DataDistillr user interface is equivalent to a query barrel in API routes and
        responses.

        Parameters:
            barrel_token (int): Token that uniquely identifies query barrel. A dictionary with all
            query barrel tokens can be found using the get_tab_token_dict() function.

        Returns:
            int: Token of most recent query in query barrel.
        """

        queries_page = self.QUERY_BARRELS + "/" + str(barrel_token)
        queries_response = self.session.get(url=queries_page)
        queries_response_json = queries_response.json()
        # Finds the part regarding the queries
        queries_list = queries_response_json["queryBarrel"]["queries"]
        # Finds token of most recent query
        query_token = queries_list[-1]["token"]
        return query_token

    def _get_query_results(self, url_endpoint: str, attempts: int) -> dict:
        """
        Returns results of previously ran query.

        Parameters:
            url_endpoint (str): API endpoint for query data

        Returns:
            pandas dataframe: Results of query.
        """

        results: dict = {'data': [], 'summary': {}}

        response = self.session.get(url=url_endpoint)

        # Grab JSON object from response
        response_data = response.json()

        # response is success and has data
        if response_data['queryRun']['status'] == 'complete':
            # add data from response to data list
            results['data'].extend(response_data['results'])
            results['summary'] = response_data['summary']

            # if response has a nextPage set... grab next page
            if response_data['summary'].get('nextPage', None) is not None:
                page_data = self._get_query_results(response_data['summary']['nextPage'],
                                                    attempts)
                results['data'].extend(page_data['data'])

                # deletes page, nextPage, and totalPages within summary
                try:
                    del results['summary']['page']
                except KeyError:
                    pass

                try:
                    del results['summary']['nextPage']
                except KeyError:
                    pass
                try:
                    del results['summary']['totalPages']
                except KeyError:
                    pass

        # Data request is still processing/running. Will try in a few seconds
        elif response_data['queryRun']['status'] == 'running':
            print("running")
            time.sleep(self.SLEEP_TIMER)

            if attempts < self.MAX_ATTEMPTS:
                results = self._get_query_results(url_endpoint, attempts + 1)
            else:
                # Number of attempts exceeded.  Exit potential infinite loop
                raise Exception('failed after', self.MAX_ATTEMPTS, 'failed attempts')
        # response is an unexpected error
        else:
            raise Exception('server response is', response_data)

        return results

    def _execute_query(self, barrel_token, query_token):
        """
        Executes query. Execute means to run query and get results of query.

        Parameters:
            barrel_token (int): Token the uniquely identifies query barrel. A dictionary with
            all query barrel tokens can be found using get_tab_token_dict(). A tab in the
            DataDistillr user interface is equivalent to a query barrel in API routes and
            responses.

            query_token (int): Token the uniquely identifies query in query barrel.

        Returns:
            pandas dataframe: Formatted results of query.

        """

        # runs query
        query_run_page = self.QUERY_BARRELS + "/" + str(barrel_token) + "/query/" + \
            str(query_token) + "/run"
        query_run = self.session.get(url=query_run_page)
        query_run_json = query_run.json()
        run_request_token = query_run_json["requestToken"]

        # gets result of query
        query_results = self.QUERY_RUN_PAGE + "/" + str(run_request_token)
        attempts = 0
        results = self._get_query_results(query_results, attempts)

        # format query results
        schema = results['summary']['columnNames']
        data = results['data']
        return pd.DataFrame(data, columns=schema)

    def execute_existing_query(self, tab_token):
        """

        Executes most recent query in a tab. The tab is identified by tab_token. A tab in the
        DataDistillr user interface is equivalent to a query barrel in API routes and
        responses.

        Parameters:
            tab_token: Token the uniquely identifies query barrel. A dictionary with
            all tab tokens can be found using get_tab_token_dict().

        Returns:
            pandas dataframe: Formatted results of query.

        """

        query_token = self._get_recent_query_token(tab_token)
        return self._execute_query(tab_token, query_token)

    def execute_new_query(self, tab_name, query):
        """

        Creates new tab named tab_name and executes query in tab.
        A tab in the DataDistillr user interface is equivalent to a query barrel in API routes and
        responses.

        Parameters:
            tab_name (str): Name of new tab
            query (int): SQL statement to be run in tab.

        Returns:
            pandas dataframe: Formatted results of query.
        """

        query_barrel_details = {
            "projectSlug": self.name.lower().replace(' ', '-'),
            "projectToken": self.project_token,
            "name": tab_name,
            "active": True,
            "icon": "type-icon-file",
            "query": "  " + query
        }

        query_barrel_resp = self.session.post(url=self.QUERY_BARRELS, json=query_barrel_details,
                                              verify=False)
        query_barrel_resp_json = query_barrel_resp.json()
        barrel_token = query_barrel_resp_json["queryBarrel"]["queries"][0]["queryBarrelToken"]
        query_token = query_barrel_resp_json["queryBarrel"]["queries"][0]["token"]

        return self._execute_query(barrel_token, query_token)

    def get_data_source_token_dict(self):
        """
        Returns dictionary with data source tokens as keys and data source names as values.

        Returns:
            dictionary (int -> str): Dictionary with data source tokens as keys and data source
            ames as values.
        """

        get_data_sources = self.PROJECT_PAGE + "/" + str(self.project_token) + "/dataSource"
        data_sources_response = self.session.get(url=get_data_sources)
        data_sources_response_json = data_sources_response.json()
        data_sources = data_sources_response_json["dataSources"]
        for data_source in data_sources:
            self.data_source_token_dict[data_source["token"]] = data_source["name"]
        return self.data_source_token_dict

    def get_data_source_token(self, data_source_name):
        """
        Returns data source token that matches data_source_name

        Returns:
            int: data source token
        """

        data_source_token_dict = self.get_data_source_token_dict()
        for token, name in data_source_token_dict.items():
            if data_source_name == name:
                return token
        raise Exception("token not found")

    def _get_presigned_urls(self, data_source_token, file_paths):
        """
        Returns list of AWS presigned urls for each file path in list of file paths

        Returns:
            array (str): list of presigned urls
        """

        # building array of file objects for post request
        files_array = []
        for file_path in file_paths:
            file_size = os.path.getsize(file_path)
            file_name = ntpath.basename(file_path)
            file_obj = {
                "name": file_name,
                "size": file_size,
                "type": "text/csv",
                "path": "/"
            }

            files_array.append(file_obj)
        files = {"files": files_array}

        post_data_source = self.DATA_SOURCE_PAGE + "/" + str(data_source_token) + "/file"
        response = self.session.post(post_data_source, json=files, verify=False)
        presigned_urls = response.json()["presignedUrls"]
        return presigned_urls

    def upload_files(self, data_source_token, file_paths):
        """
        Uploads list of files to a data source.

        Parameters:
            data_source_token (int): Token the uniquely identifies data source.
            file_paths (array): List of absolute file paths of files to be uploaded.

        Returns:
            boolean: True if file was uploaded successfully.
        """

        presigned_urls = self._get_presigned_urls(data_source_token, file_paths)
        for i, file_path in enumerate(file_paths):
            presigned_url = presigned_urls[i]
            with open(file_path, encoding="utf-8") as file:
                file_data = file.read()
                response = self.session.put(presigned_url,
                                            data=file_data,
                                            headers={'content-type': 'text/plain'})

            if not response.ok:
                raise Exception("file not uploaded")
        return 'file uploaded successfully'
