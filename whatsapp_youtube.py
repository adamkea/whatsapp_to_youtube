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
            authorization_prompt_message=""
        )
        
        flow.run_local_server(port=8080, prompt="consent")

        credentials = flow.credentials

        with open("token.pickle", "wb") as f:
            print("Saving Credentials for Future Use...")
            pickle.dump(credentials, f)

youtube = build('youtube', 'v3', credentials=credentials)

links = []

with open("lorcan.txt", encoding="utf8") as f:
    lines = f.readlines()
    for l in lines:
        if "youtube.com" in l:
            link = re.findall("(?P<url>https?://[^\s]+)", l)
            try:
                video_id = link[0].split('?v=')[1].split('&')[0]
                links.append(video_id)
            except:
                print("An exception occured")

    # # get users playlists
    request = youtube.playlists().list(part="id, snippet", mine=True)
    my_playlists = request.execute()
    
    # create the playlist
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

    playlist_id = response.get('id')

    batch = youtube.new_batch_http_request()

    for link in links:
        try:
            youtube.playlistItems().insert(
                part="snippet",
                body={
                        'snippet': {
                        'playlistId': playlist_id, 
                        'resourceId': {
                                'kind': 'youtube#video',
                            'videoId': link
                            }
                        }
                }
                ).execute()
            print('Video added')
        except:
            print('Video could no be added')

    responses = batch.execute()

print(links)
print(len(links))