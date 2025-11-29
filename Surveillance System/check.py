"""Lightweight wrapper to run the main surveillance loop.

This file used to contain a quick serial+camera check. The
implementation has been modularized: serial handling now lives
in `main.py` and camera/recording is in `helpers/camera.py`.

Run this file to start the main surveillance loop (same behavior
as the previous quick-check script).
"""

from main import main

if __name__ == '__main__':
    main()