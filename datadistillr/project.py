
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
