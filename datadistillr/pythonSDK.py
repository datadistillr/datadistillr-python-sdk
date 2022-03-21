import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from collections import namedtuple
from json import JSONEncoder



class datadistillr:
    """url pages based off the base url"""
    base_url = "https://app.datadistillr.io/api/"
    login_page = base_url + "login"
    organizations_list = organizations = base_url + "organization"
    logout_page = base_url + 'logout'

    

    def __init__(self, email, password):
        """Creates session"""
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.session = requests.Session()    # stores the cookies so you can make requests (pass around cookie)
        self.email = email
        self.password = password
        self.login_resp = self.login()
        pass


    def login(self):
        """Takes in email and password, converts to dictionary, then converts to JSON, and posts the user info to the login page"""
        print("logging in ...")
        user_info = {
            "email": self.email, 
            "password": self.password,
            "invitations":{
             "organizationInvitationToken":None,
             "projectInvitationToken":None,
             "teamInvitationToken":None}
            }
       
        login_response = self.session.post(url = self.login_page, json = user_info, verify= False)
        print("login cookies " + str(self.session.cookies))

        #Converts response to JSON
        login_resp_json = login_response.json()

        #returns login json
        return login_resp_json

    def logout(self):
        """Gets logout page"""
        logout_response = self.session.get(url = self.logout_page, verify = False)
        #Converts response to JSON
        logout_resp_json = logout_response.json()
        #Parses the JSON response into a python dictionary
        return logout_resp_json


    # Returns a list of project objects to which the user has access.
    def get_projects(self):
        """Gets projects page"""

        # check if login is correct
        if not self.login_resp["loggedIn"]: 
          return "login is incorrect"

        # URL to get project needs active org token, URL format may change according to Sanaa, example : https://app.datadistillr.io/api/organization/880610291/projects
        orgToken = self.login_resp["activeOrganization"]["token"]
        projects_page = self.base_url + "organization/" + str(orgToken) + "/projects"
        projects_response = self.session.get(url = projects_page, verify = False)
        print("get projects cookies " + str(self.session.cookies))

        # Converts response to JSON
        proj_resp_json = projects_response.json()


        # Gets the projects list
        proj_list = proj_resp_json["projects"]
        proj_object_list = []

        for i in range(len(proj_list)):
          proj_object = project(proj_list[i], self.session) # create new project object with json
          proj_object_list.append(proj_object)
          
        # Returns list of the project object
        return proj_object_list
    

    # Retrieves an individual project object
    def get_project(self, project_name):

      # check if login is correct
      if not self.login_resp["loggedIn"]: 
          return "login is incorrect"

      proj_list = self.get_projects()
      for i in range(len(proj_list)):
        proj_object = proj_list[i]
        if proj_object.name == project_name:
          return proj_object
      return "project not found"



    # Returns a list of organizations the user has access.
    def get_organizatons(self):

        # check if login is correct
        if not self.login_resp["loggedIn"]: 
          return "login is incorrect"

        organizations_response = self.session.get(url = self.organizations_list, verify = False)
        print("get org " + str(self.session.cookies))

        organizations_resp_json = organizations_response.json()
        return organizations_resp_json["organizations"]

    def get_teams(self):
      print("get teams function")



class project:

      def __init__(self, proj_details, curr_session):
        self.session = curr_session  # stores the cookies so you can make requests (pass around cookie)
        self.details_json = proj_details
        self.name = self.details_json["name"]
      
        pass
        
      
      # This function returns a pandas data frame of the data set from the query.
      # getData(<query name>)
      def get_data(self, query_name): 
         print("project details:")
         print(self.details_json)
         print("query name:")
         print(query_name)
        # call get project detail for the project i want to send message to
        # STEP 1: Find query barrel token for project (ex: carriers)
        # projects_page = self.base_url + “organization/” + str(orgToken) + “/projects/” + str(projToken)
        # for (projects_page response) find where name = query_name --> return query barrel token based on that name 

        # STEP 2: get query barrel info
          # querybarrelresp = get (https://app.datadistillr.io/api/queryBarrels/<1482240829>(querybarrel token))

        # STEP 3: find all queries within barrel
          # queriesquerybarrelresp['queryBarrel']['queries']

        # STEP 4: find where the query is active
          # for (query in queries) --> find where query["active"] = true --> resultsURL =  query["resultsUrl"]

        # STEP 5: Get results based on active query
          # get(resultsURL)
      
      



#To test features, enter info below. 

# Enter dataDistillr account login info here  
my_email = '...'
my_pass = '...'
ddr = datadistillr(my_email, my_pass)

print()
print("project list:")
print(ddr.get_projects())

print()
print("Project Name:")
project = ddr.get_project("Projects") # enter project name here
project.get_data("Data Source Here")

print()
print("organizations list:")
print(ddr.get_organizatons())

print()
#print("Send Message to project")
#message = 'I like cats'
#print(project.send_message(message))
