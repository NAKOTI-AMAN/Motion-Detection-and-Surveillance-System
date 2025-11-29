import os
from typing import Optional

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def upload_file(file_path: str, mime_type: str = 'video/mp4', folder_id: Optional[str] = None) -> str:
	"""Upload a file to Google Drive using a service account and return a shareable link.

	Expects the service account JSON path in the environment variable
	`GOOGLE_SERVICE_ACCOUNT_FILE`. Optionally a `DRIVE_FOLDER_ID` can be
	provided to place the file in a specific Drive folder.
	"""
	sa_file = os.environ.get('GOOGLE_SERVICE_ACCOUNT_FILE')
	if not sa_file:
		raise RuntimeError('GOOGLE_SERVICE_ACCOUNT_FILE not set in environment')

	scopes = ['https://www.googleapis.com/auth/drive']
	creds = Credentials.from_service_account_file(sa_file, scopes=scopes)
	service = build('drive', 'v3', credentials=creds)

	file_metadata = {
		'name': os.path.basename(file_path)
	}
	if folder_id:
		file_metadata['parents'] = [folder_id]

	media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
	created = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
	file_id = created.get('id')

	# Make file readable by anyone with the link
	try:
		service.permissions().create(fileId=file_id, body={
			'type': 'anyone',
			'role': 'reader'
		}).execute()
	except Exception:
		# permission setting is best-effort; continue even if it fails
		pass

	link = f'https://drive.google.com/file/d/{file_id}/view?usp=sharing'
	return link

