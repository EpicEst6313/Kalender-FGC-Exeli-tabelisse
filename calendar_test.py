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

# Ids for calendars
calendar_ids = []
events = []


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

def main():
    #code wide varribles
    global calendar_ids, events

    # Making sure that program has access
    credentials = authorization_controll()
    service = build (
        "calendar",
        "v3",
        credentials=credentials
    )

    # Asking user as long as teher is calendar name that matches
    while True:

        # Asking user which calenders are wanted to use by this program split in teh end splits it 
        summary = input("Kalendri nimed millest soovid, et info pannakse Exeli tabelisse(eralda komaga): ").split(",")

        # Asking all the calendars to make calendar summary to id
        response = service.calendarList().list().execute() # Creates request object and execute gives the response directly to varible

        print("Kasutan nende kalendrite infot:")

        # Taking the response list of dictonarys item dictonary open and comparing summary names to user names for accurate id to request later
        for calendar in response["items"]:
            for name in summary:
                if calendar.get("summary").lower() == name.lower().strip():
                    print(calendar.get("summary"))
                    calendar_ids.append(calendar.get("id"))
        
        if (calendar_ids):
            break
        
    # Getting only the right calendar and it's events
    for calendar_id in calendar_ids:
        events.append(service.events().list(calendarId = calendar_id).execute())
    
    # Printing out beautifully
    print("Kuupaev".ljust(20), "Algus".ljust(10), "Lopp".ljust(10), "sundmus".ljust(30), "Kalender")

    # printing all events out seperetly
    for calendar_events in events:
        for event in calendar_events["items"]:
            prinditav_sona = "".ljust(20) + event["start"].get("dateTime").ljust(10) + event["end"].get("dateTime").ljust(10) + event.get("summary").ljust(30)
            print(
                event.get("summary"), # what event
                event.get("start"), # when starts
                event.get("end") # when ends
            )


main()
