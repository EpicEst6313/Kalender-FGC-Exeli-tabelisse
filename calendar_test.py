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
TOKEN_FILE = SECRETS_DIR / "calendar_token.json" # Location of the stored authentication token (user premissions given to access stuff asked)

# Scopes that say what this apps wants to do
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly"
]


# Controlling token existence
if (TOKEN_FILE.exists()):
    credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Controlling if the credentials are valid
    if (credentials.valid):
        print("tootab")
    
    # Requesting new ones if not valid
    elif (credentials.expired and credentials.refresh_token):
        credentials.refresh(Request())
    
    # if no refresh token then letting user login again
    else:
        print("lasen kasutajal sisse logida")

# if no token then letting user login
else:
    print("lasen kasutajal sisse logida")