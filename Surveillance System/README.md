# Surveillance System

- **Purpose:**: Lightweight motion-triggered surveillance that records short video clips when motion is signaled over a serial connection, uploads the clip to Google Drive, and sends a notification email with the Drive link.

**How It Works**
- The main loop in `main.py` listens to a serial port for the exact string `MOTION`.
- When `MOTION` is received the helper `helpers/camera.py` records a short video (default 10s).
- After recording the file is uploaded to Google Drive using `utils/drive.py` (service account).
- If configured, `utils/mail.py` sends an alert email (Mailgun) with the Drive file link.

**Files / Modules**
- `main.py`: serial listener and orchestrator (records -> upload -> alert)
- `check.py`: simple wrapper to run `main()` (kept for compatibility)
- `helpers/camera.py`: `record_video(...)` — handles camera capture and preview
- `utils/drive.py`: `upload_file(...)` — uploads a file to Google Drive and returns a shareable link
- `utils/mail.py`: `send_mail(...)` — sends an alert via Mailgun
- `.env`: environment variables (placeholders included)

**Required Environment Variables**
- `GOOGLE_CLIENT_FILE`: path to client credentials JSON (required for Drive uploads)
- `DRIVE_FOLDER`: Optional Drive folder to upload into (leave blank to upload to root)
- `MAILGUN_API_KEY`: Mailgun private API key
- `MAILGUN_DOMAIN`: Mailgun domain (e.g. `mg.example.com`)
- `MAILGUN_FROM`: From address for alerts (e.g. `Alert <alerts@mg.example.com>`)
- `ALERT_TO_EMAIL`: Destination email to receive alert notifications
- `PORT`: Serial port (default `COM9`)
- `BAUDRATE`: Serial baud (default `115200`)

**Setup**
1. Install Python dependencies:

```bat
cd "Surveillance System"
python -m pip install -r requirements.txt
```

2. Configure secrets and values in `.env` (do not commit `.env`):
- Place your Google client credentials JSON somewhere safe and set `GOOGLE_CLIENT_FILE` to its path.
- Add your `client_email` to test user in Oauth consent screen.
- Set Mailgun settings (`MAILGUN_API_KEY`, `MAILGUN_DOMAIN`, `MAILGUN_FROM`) and `ALERT_TO_EMAIL`.

3. Note: `credentials.json` and `token.json` is ignored in `.gitignore` to prevent accidental commits.

**Run**
- From Windows `cmd.exe` in the `Surveillance System` folder:

```bat
python main.py
```

**Preview & Controls**
- The camera preview window appears during recording (if your environment supports OpenCV GUI).
- Press `q` in the preview window to stop recording early.
- If running headless (no GUI), the preview is automatically disabled and recording continues.

**Troubleshooting**
- Serial port errors: confirm the correct COM port and baud rate, and that the device sends a newline-terminated `MOTION` line.
- Mailgun errors: verify API key and domain are correct and that Mailgun account is configured to send to the recipient.

