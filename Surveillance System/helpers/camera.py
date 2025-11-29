import os
import time
from datetime import datetime

import cv2


def _surveillance_base_dir():
	# parent directory of this helpers folder -> Surveillance System/
	return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def record_video(output_name: str = None, duration: float = 10.0, fps: float = 20.0, resolution=(640, 480), camera_index: int = 0):
	"""Record video from the camera and save it to the Surveillance System folder.

	- output_name: filename (e.g. 'intruder.mp4'). If None, a timestamped name is used.
	- duration: seconds to record.
	- fps: frames per second for the writer.
	- resolution: (width, height) tuple.
	- camera_index: camera device index for cv2.VideoCapture.

	During recording a preview window is shown. Press 'q' in the preview
	window to stop recording early.

	Returns the absolute path to the saved file.
	"""
	base_dir = _surveillance_base_dir()
	if output_name:
		filename = output_name
	else:
		ts = datetime.now().strftime('%Y%m%d_%H%M%S')
		filename = f'intruder_{ts}.mp4'

	out_path = os.path.join(base_dir, filename)

	cap = cv2.VideoCapture(camera_index)
	if not cap.isOpened():
		raise RuntimeError(f"Unable to open camera index {camera_index}")

	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	out = cv2.VideoWriter(out_path, fourcc, fps, resolution)

	start = time.time()
	window_name = 'Surveillance Preview'
	preview_enabled = True

	try:
		while time.time() - start < duration:
			ret, frame = cap.read()
			if not ret:
				# small sleep to avoid busy loop if frames fail
				time.sleep(0.01)
				continue

			# Resize frame if it's not the desired resolution
			if (frame.shape[1], frame.shape[0]) != resolution:
				frame = cv2.resize(frame, resolution)

			out.write(frame)

			# show preview (best-effort; continue if GUI not available)
			if preview_enabled:
				try:
					cv2.imshow(window_name, frame)
					# waitKey required to refresh window; use small delay
					if cv2.waitKey(1) & 0xFF == ord('q'):
						# user requested early stop
						break
				except cv2.error:
					# if the environment doesn't support GUI windows, disable preview
					preview_enabled = False
					try:
						cv2.destroyAllWindows()
					except Exception:
						pass

	finally:
		cap.release()
		out.release()
		try:
			cv2.destroyAllWindows()
		except Exception:
			pass

	return out_path

