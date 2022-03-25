
class project:

    def __init__(self, proj_details, curr_session):
        # stores the cookies so you can make requests (pass around cookie)
        self.session = curr_session
        self.details_json = proj_details
        self.name = self.details_json["name"]
        self.project_token = self.details_json["token"]

        pass
