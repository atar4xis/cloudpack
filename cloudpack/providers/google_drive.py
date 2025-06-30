from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

service = None


def init_oauth(client_id, client_secret, redirect_uri):
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uris": [redirect_uri],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        "https://www.googleapis.com/auth/drive.file",
    )

    creds = flow.run_local_server(port=0)  # let the OS choose an available port
    return creds


def auth(config):
    global service

    creds = init_oauth(
        config.get("client_id"), config.get("client_secret"), "http://localhost"
    )

    if not creds:
        return False

    try:
        service = build("drive", "v3", credentials=creds)
        return True
    except HttpError as error:
        print(f"An error occurred: {error}")
        return False


def get_cloudpack_folder_id():
    if not service:
        print("Google Drive service not initialized. Please authenticate first.")
        return False

    query = "name = 'cloudpack' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    response = (
        service.files()
        .list(q=query, spaces="drive", fields="files(id, name)")
        .execute()
    )
    files = response.get("files", [])

    if files:
        return files[0]["id"]
    else:
        # create the folder if it doesn't exist
        file_metadata = {
            "name": "cloudpack",
            "mimeType": "application/vnd.google-apps.folder",
        }
        folder = service.files().create(body=file_metadata, fields="id").execute()
        return folder.get("id")


def upload(file_path, file_name=None):
    if file_name is None:
        file_name = Path(file_path).name

    if not service:
        print("Google Drive service not initialized. Please authenticate first.")
        return False

    try:
        media = MediaFileUpload(file_path, mimetype="application/octet-stream")
        service.files().create(
            body={"name": file_name, "parents": [get_cloudpack_folder_id()]},
            media_body=media,
            fields="id",
        ).execute()
        return True
    except HttpError as error:
        print(f"An error occurred: {error}")
        return False
