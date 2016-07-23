from LaracastsScraper import ConfigLoader
import requests
import sys

"""
Authenticate a session with the given URL so that our
requests will use the same session throughout the program.

Returns the authenticated session.
Exits with an error code if the request fails.

Arguments:
    - session The requests session to authenticate
"""
def authenticate_session(session, url):

    print("Authenticating session with " + str(url) + "...")

    # Get the login information and authenticate.
    email, password = ConfigLoader.get_login_information()
    login_data = {'email': email, 'password': password}

    request = session.post(url, data=login_data, verify=False)

    if request.status_code in [200, 201]:
        print "Authentication successful.\n"
        return session

    print("Authentication failed. Error: " + str(request.status_code))
    print("Exiting program.")

    sys.exit(1)


"""
Create a new Requests session for this URL.
This passes a new Session object to authenticate_session() above.
"""
def create_session(url):
    return authenticate_session(requests.Session(), url)

