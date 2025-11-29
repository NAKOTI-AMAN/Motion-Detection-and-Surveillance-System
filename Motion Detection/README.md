# This is the motion detection part of the complete system
## This part was made in mbed os and keil studio, follow the steps below:
1. Login to os.mbed.com and go to keil studio cloud create a new mbed os project.
2. Copy the code in main.cpp file here and paste it in the main.cpp file of your project.
3. Click on build target and select NUCLEO-F401RE.
4. Then click on build project.
5. Make connects for your circuit (shown in the image, i.e. circuit_connection.jpg).
5. Connect NUCLEO-F401RE development board to your system and then click run project.

If your run project fails then in your system file manager go to downloads or where your bin file is downloaded, copy that file and save it in the bootloader drive of your stm32 nucleo-f401re board (which will appear after connecting it with your system).