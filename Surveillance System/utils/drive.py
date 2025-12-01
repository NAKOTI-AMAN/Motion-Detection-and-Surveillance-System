import os
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def upload_file(file_path: str, mime_type: str = 'video/mp4', folder: Optional[str] = None) -> str:
	
	creds = None
	SCOPES = ['https://www.googleapis.com/auth/drive']
	CREDENTIALS_FILE = os.environ.get('GOOGLE_CLIENT_FILE', 'credentials.json')

	if not CREDENTIALS_FILE or not os.path.exists(CREDENTIALS_FILE):
		raise FileNotFoundError("credentials.json path invalid or not found in .env")
	
	if os.path.exists('./token.json'):
		creds = Credentials.from_authorized_user_file('./token.json', SCOPES)

	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.json', 'w') as token:
			token.write(creds.to_json())

	try:
		service = build("drive", "v3", credentials=creds)

		response = service.files().list(
			q=f"name='{folder}' and mimeType='application/vnd.google-apps.folder'",
			spaces='drive'
		).execute()

		if not response.get('files'):
			folder_metadata = {
				'name': f"{folder}",
				'mimeType': 'application/vnd.google-apps.folder'
			}
			folder = service.files().create(body=folder_metadata, fields="id").execute()
			folder_id = folder['id']
		else:
			folder_id = response['files'][0]['id']

		# Upload file and print shareable link
		file_name = os.path.basename(file_path)
		file_metadata = {"name": file_name}

		if folder_id:
			file_metadata["parents"] = [folder_id]

			media = MediaFileUpload(file_path, mimetype=mime_type)
			upload = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
			file_id = upload.get('id')
			service.permissions().create(
				fileId=file_id,
				body={'type': 'anyone', 'role': 'reader'}
			).execute()

			
			share_link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

			return share_link

	except HttpError as e:
		print("Error: " + str(e))

