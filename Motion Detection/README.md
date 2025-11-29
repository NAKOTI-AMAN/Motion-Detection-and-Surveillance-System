# Motion Detection System Setup

This document provides instructions for setting up and deploying the motion detection component of the complete system using **Mbed OS** and **Keil Studio Cloud** on the **NUCLEO-F401RE** development board.

---

## Prerequisites

Before you begin, ensure you have:

* An account on **os.mbed.com**.
* Access to **Keil Studio Cloud**.
* The **NUCLEO-F401RE** development board.
* The necessary circuit components (as shown in the connection diagram).
* The `main.cpp` source code for the motion detection logic (to be provided separately).

---

## Step-by-Step Setup

Follow these steps to build and deploy the project:

### 1. Project Creation in Keil Studio Cloud

1.  Log in to **os.mbed.com**.
2.  Navigate to **Keil Studio Cloud**.
3.  Create a **new Mbed OS project**.

### 2. Code Integration

1.  Open the newly created project's `main.cpp` file.
2.  **Copy the provided motion detection source code** and paste it into the project's `main.cpp` file, replacing any existing content.

### 3. Project Build

1.  Click on **"Build Target"** (or equivalent option).
2.  Select the **NUCLEO-F401RE** as the target board.
3.  Click on **"Build Project"**.

---

## Hardware Configuration

Establish the hardware connections for your motion detection circuit using the NUCLEO-F401RE board.



**Refer to the image circuit_diagram.jpeg for the correct component connections.**

---

## Deployment and Run

1.  Connect the **NUCLEO-F401RE** development board to your system via USB.
2.  In Keil Studio Cloud, click **"Run Project"**.

### Troubleshooting Deployment (Manual Flash)

If the **"Run Project"** step fails to deploy the code directly:

1.  Locate the downloaded `.bin` file in your system's file manager (typically in the **Downloads** folder).
2.  Your connected **NUCLEO-F401RE** board will appear as a removable drive named **'NUCLEO'** or similar (this is the ST-Link Bootloader drive).
3.  **Copy the downloaded `.bin` file** and **paste it into the NUCLEO board's drive**.
4.  The board will automatically flash the new firmware and restart the program.