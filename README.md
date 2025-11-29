# Motion Detection and Surveillance System

This repository implements a two-part system for motion detection and automated surveillance.

- Part 1: Follow the instructions in `Motion Detection/README.md` (hardware/microcontroller side).
- Part 2: Then follow the instructions in `Surveillance System/README.md` (host PC / Python side).

Overview
-
This system detects motion using a PIR sensor connected to a microcontroller (STM32 Nucleo-F401RE). When the PIR sensor detects motion, the microcontroller sends a flag over the serial port to a PC. A Python script running in the background on the PC listens on the serial port, receives the flag, and takes the following actions:

1. Turn on the PC camera and record video for 10 seconds.
2. Upload the recorded video to cloud storage.
3. Send the cloud link to the registered email address as an intruder alert.

Repository structure (high level)
- `Motion Detection/` — microcontroller code and hardware notes (PIR sensor, wiring, firmware). See `Motion Detection/README.md`.
- `Surveillance System/` — Python scripts, helpers, and utilities that run on the PC. See `Surveillance System/README.md`.

Hardware & software flow (concise)
- PIR sensor detects motion → STM32 Nucleo-F401RE firmware raises a flag.
- MCU writes the flag to the PC's serial port.
- Background Python listener reads the serial flag, activates the PC camera for 10 seconds and records video.
- The recording is uploaded to cloud storage and a link is emailed to the registered address as an alert.

Files you will likely use first
- `Motion Detection/main.cpp` — microcontroller firmware example.
- `Surveillance System/main.py` — main Python listener and recorder.
- `Surveillance System/requirements.txt` — required Python packages for the surveillance side.

Notes and tips
- Keep your `.env` file (credentials, API keys, email config, serial port settings) private and do not commit it to the repository.
- For development, create and use a Python virtual environment for the `Surveillance System` code.
- Follow the `Motion Detection/README.md` first (set up hardware and firmware), then continue with `Surveillance System/README.md` to configure and run the PC-side software.
