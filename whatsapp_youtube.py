import os, re, pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

credentials = None

# handle oauth credentials thanks to Corey Schafer: https://www.youtube.com/watch?v=vQQEaSnQ_bs
if os.path.exists("token.pickle"):
    print("Loading Credentials From File...")
    with open("token.pickle", "rb") as token:
        credentials = pickle.load(token)

if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print("Refreshing Access Token...")
        credentials.refresh(Request())
    else:
        print("Fetching New Tokens...")
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json",
            scopes=["https://www.googleapis.com/auth/youtube.force-ssl"],
        )
        
        flow.run_local_server(port=8080, prompt="consent")

        credentials = flow.credentials

        with open("token.pickle", "wb") as f:
            print("Saving Credentials for Future Use...")
            pickle.dump(credentials, f)

youtube = build('youtube', 'v3', credentials=credentials)

regex = "(?P<url>https?://[^\s]+)"
links = []

with open('whatsapp.txt', encoding="utf8") as f:
    lines = f.readlines()
    for l in lines:
        if "youtube.com" in l:
            link = re.findall(regex, l)
            try:
                links.append(link[0])
            except:
                print("An exception occured")
    
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": "Sample playlist created via API",
            "description": "This is a sample playlist description.",
            "tags": [
              "sample playlist",
              "API call"
            ],
            "defaultLanguage": "en"
          },
          "status": {
            "privacyStatus": "private"
          }
        }
    )
    response = request.execute()

    print(response)

print(links)