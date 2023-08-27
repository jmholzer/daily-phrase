from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Load your client secrets
flow = InstalledAppFlow.from_client_secrets_file('credentials/daily-phrase-secrets.json', ['https://www.googleapis.com/auth/youtube.upload'])

# Run the OAuth 2.0 flow
credentials = flow.run_local_server(port=8080)

# Check if the credentials are valid and store the refresh token
if not credentials.valid:
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        raise ValueError("Failed to authenticate.")

refresh_token = credentials.refresh_token
print("Refresh Token:", refresh_token)

