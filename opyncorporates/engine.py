from opyncorporates.versions import versions


def create_engine(api_version="0.4", api_token=None, ):
    """ Factory function to create an Version object.

    The factory function allows a user to select the API version to use
    for the user's requests. The default version is 0.4.

    Parameters
    ----------
    api_token: str (optional)
        The API token used for the request.
    api_version: str (optional)
        The API version used for the request.

    """

    return versions[api_version](api_token=api_token)