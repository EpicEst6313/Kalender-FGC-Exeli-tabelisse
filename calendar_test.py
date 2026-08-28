from pathlib import Path
# For working with files and directories in a platform-independent way

from google.auth.transport.requests import Request
# For making the request needed to refresh an expired access token

from google.oauth2.credentials import Credentials
# For storing/loading the authentication credentials used to access Google APIs

from google_auth_oauthlib.flow import InstalledAppFlow
# For performing the initial OAuth login and authorization

from googleapiclient.discovery import build
# For creating a client used to communicate with the Google Calendar API


# Paths needed for authentication
SECRETS_DIR = Path.home() /"GoogleCalendarSheetsSecrets" # Location of the secrets
CREDENTIALS_FILE = SECRETS_DIR / "credentials.json" # Location of the credentials file
TOKEN_FILE = SECRETS_DIR / "calendar_token.json" # Location of the stored authentication token (user permissions given to access stuff asked)

# Scopes that say what this apps wants access to
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly"
]


def login():
    """
    Function for letting user login and give permission and saving it to disk
    """
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES) # Preparing the OAuth authorization flow
    credentials = flow.run_local_server() # Starting the local OAuth server and opening the authorization flow
    TOKEN_FILE.write_text(credentials.to_json()) # Saving the credentials as JSON so we can reuse them next time
    return credentials

def authorization_controll():
    """
    Function for controlling the existence of credentials and if needed and possible refreshing them
    otherwise calling login function
    """

    # Controlling token existence
    if (TOKEN_FILE.exists()):
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        # Controlling if the credentials are valid
        if (credentials.valid):
            return credentials
        
        # Requesting new ones if not valid
        elif (credentials.expired and credentials.refresh_token):
            credentials.refresh(Request()) # Requesting tokencredentials.jsoncredentials.json refreshin if possible
            TOKEN_FILE.write_text(credentials.to_json()) # Saving the refreshed credentials as JSON so we can reuse them next time
            return credentials

        # If couldn't refresh token then letting user login
        else:
            return login()

    # If no token is found, letting user login
    else:
        return login()