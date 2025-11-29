import os
import time
from datetime import datetime

import serial
from dotenv import load_dotenv
from helpers import camera
from utils import drive, mail

load_dotenv()


def main(port: str = None, baudrate: int = None, record_duration: float = 10.0):
	"""Main surveillance loop: read serial flag and record when motion is detected.

	Uses environment variables (can be set in `.env`):
	- PORT (overrides default COM port)
	- BAUDRATE
	- DRIVE_FOLDER_ID (optional)
	- ALERT_TO_EMAIL (destination email for alerts)
	"""
	port = port or os.environ.get('PORT', 'COM9')
	baudrate = baudrate or int(os.environ.get('BAUDRATE', '115200'))
	drive_folder = os.environ.get('DRIVE_FOLDER_ID')
	alert_to = os.environ.get('ALERT_TO_EMAIL')

	try:
		ser = serial.Serial(port, baudrate, timeout=1)
	except Exception as e:
		print(f"Error opening serial port {port}: {e}")
		return

	print(f"Listening on {port} at {baudrate}bps. Waiting for 'MOTION' lines...")

	try:
		while True:
			try:
				raw = ser.readline()
			except Exception as e:
				print(f"Serial read error: {e}")
				time.sleep(1)
				continue

			if not raw:
				# nothing received, continue
				continue

			data = raw.decode(errors='ignore').strip()
			if not data:
				continue

			if data == 'MOTION':
				print("Motion Detected — Recording video for {} seconds".format(record_duration))
				ts = datetime.now().strftime('%Y%m%d_%H%M%S')
				filename = f'intruder_{ts}.mp4'
				try:
					saved_path = camera.record_video(output_name=filename, duration=record_duration)
					print(f"Recording saved: {saved_path}")
				except Exception as e:
					print(f"Failed to record video: {e}")
					continue

				# upload to Google Drive
				try:
					drive_link = drive.upload_file(saved_path, folder_id=drive_folder)
					print(f"Uploaded to Drive: {drive_link}")
				except Exception as e:
					print(f"Drive upload failed: {e}")
					drive_link = None

				# send alert email with link
				if alert_to and drive_link:
					subject = f"Surveillance Alert: motion detected {ts}"
					body = f"Motion was detected and a recording was saved. Drive link: {drive_link}"
					try:
						resp = mail.send_mail(alert_to, subject, body)
						print(f"Alert email sent: {resp}")
					except Exception as e:
						print(f"Failed to send alert email: {e}")
				else:
					print("No alert email sent (missing ALERT_TO_EMAIL or drive link)")
			else:
				print("No motion Detected")

	except KeyboardInterrupt:
		print("Stopping surveillance (KeyboardInterrupt)")
	finally:
		try:
			ser.close()
		except Exception:
			pass


if __name__ == '__main__':
	main()
