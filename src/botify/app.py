import requests
import base64
import urllib.parse

CLIENT_ID = 'a7891efbee304e7f9ac0640cc1a4de89'
CLIENT_SECRET = 'd2374fc109f54f40a162329e8fa37702'
REDIRECT_URI = 'https://spotify.com'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
SCOPE = 'user-read-playback-state user-read-currently-playing'

def app():
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    print(f"Go to this URL to authorize: {auth_url}")

    access_token = get_access_token("AQCLGHGQtvLqP45LCUqAovXW02AhjiS_h_MEG4CGzUQ-zDbW8D1YIcjxDpfaUxT6ACGPBTgJcRBIknYTR4TkJ9C_KfzbOTfzEhJwDSMR-1QSkZ4ChqCXw3SoYfUX-ww7SKJ24_N1ETfiqswx98nHqEWApDZSCGZMxYrjZHX2j0WcpgP6JG0no8Kq9zov9hSKBgUkRfh-otoK2Q9OkXPx6x810SI8PmwRC8JGaKPa")
    print(f"Access Token: {access_token}")

    current_playback = get_current_playback(access_token)
    print(current_playback)

def get_access_token(auth_code):
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()

    headers = {
        'Authorization': f"Basic {b64_auth_str}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    if response.status_code == 200:
        token_info = response.json()
        return token_info['access_token']
    else:
        print("Failed to get token:", response.status_code, response.text)
        return None


def get_current_playback(access_token):
    SPOTIFY_API_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
    headers = {
        'Authorization': f"Bearer {access_token}"
    }
    response = requests.get(SPOTIFY_API_URL, headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 204:
        print("No content currently playing.")
        return None
    else:
        print("Failed to get playback info:", response.status_code, response.text)
        return None

