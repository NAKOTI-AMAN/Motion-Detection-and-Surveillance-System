import os
from typing import Optional

import requests


def send_mail(to_email: str, subject: str, text: str, from_email: Optional[str] = None) -> dict:
	"""Send a simple email via Mailgun and return the response JSON-like dict.

	Environment variables required:
	- MAILGUN_API_KEY
	- MAILGUN_DOMAIN
	- MAILGUN_FROM (optional if from_email provided)
	"""
	api_key = os.environ.get('MAILGUN_API_KEY')
	domain = os.environ.get('MAILGUN_DOMAIN')
	sender = from_email or os.environ.get('MAILGUN_FROM')

	if not api_key or not domain or not sender:
		raise RuntimeError('Mailgun configuration missing (MAILGUN_API_KEY, MAILGUN_DOMAIN, MAILGUN_FROM)')

	url = f'https://api.mailgun.net/v3/{domain}/messages'
	data = {
		'from': f"Mailgun Sandbox <{sender}>",
		'to': to_email,
		'subject': subject,
		'text': text
	}

	resp = requests.post(url, auth=('api', api_key), data=data)
	try:
		return {'status_code': resp.status_code, 'text': resp.text}
	except Exception:
		return {'status_code': resp.status_code}

