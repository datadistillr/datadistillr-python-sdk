
class project:
    """
    This is a class for getting project level data.

    Attributes:
        curr_session (session): Current session being used.
        proj_details (json): json containing details of project.
    """

    def __init__(self, proj_details, curr_session):
        """
        The constructor for Datadistillr class. Creates a session.

        Parameters:
            curr_session (session): Current session being used.
            proj_details (json): json containing details of project.
        """

        self.session = curr_session
        self.details_json = proj_details
        self.name = self.details_json["name"]
        self.project_token = self.details_json["token"]
