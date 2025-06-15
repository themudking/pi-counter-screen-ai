# pi-counter-screen-ai
Raspberry Pi Counter Project Testing Gemma-3-4b-it LLM to build an app from scratch

# install steps
1. Install Pillow: `sudo apt-get install python3-pil`
2. Add Images (PNG or JPG) to the img folder
2.1 Name images with a number for the order you want them to load. (1.png, 2.png, 3.png)

# run
1. open the folder in terminal
2. type `python3 counter.py`

# autostart
Autostarting Your Python GUI Application on Boot
To make your timer application run automatically when your Raspberry Pi starts up, we will create a systemd service file. This file tells the operating system what to run and when to run it.

Step 1: Save Your Python Script
First, ensure your Python script is saved in a permanent location on your Raspberry Pi. For this guide, we'll assume you have saved the script from the Canvas at the following path:

/home/pi/pi-counter-screen-ai/counter.py

(If you saved it elsewhere, remember to substitute your actual path in the steps below.)

Step 2: Create a systemd Service File
Next, you need to create a service file. Open a terminal on your Raspberry Pi and run the following command to create and edit a new file named timer.service:

sudo nano /etc/systemd/system/timer.service

Step 3: Add Content to the Service File
Copy and paste the following configuration into the nano editor:

[Unit]
Description=My Python Timer Application
After=graphical.target

[Service]
User=pi
Environment=DISPLAY=:0
ExecStart=/usr/bin/python3 /home/pi/pi-counter-screen-ai/counter.py
Restart=always

[Install]
WantedBy=graphical.target

Explanation of the file:
[Unit]
Description=My Python Counter Application
# This makes sure we wait for the graphical login screen to be ready
After=graphical.target

[Service]
# --- CRITICAL: Set the user that owns the script and will run it ---
User=counter
Group=counter

# --- CRITICAL: Set the working directory to your script's location ---
WorkingDirectory=/home/counter/counter/pi-counter-screen-ai

# --- CRITICAL: Set environment variables needed for a GUI app ---
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/counter/.Xauthority

# --- The command to execute ---
ExecStart=/usr/bin/python3 /home/counter/counter/pi-counter-screen-ai/counter.py

# --- Restart behavior ---
Restart=on-failure
RestartSec=10

[Install]
WantedBy=graphical.target

After pasting the text, save the file by pressing Ctrl+X, then Y, then Enter.

Step 4: Enable and Start the Service
Now that the service file is created, you need to tell systemd to use it. Run the following commands in your terminal one by one:

Reload the systemd manager to read your new file:

sudo systemctl daemon-reload

Enable your service to start on every boot:

sudo systemctl enable timer.service

Start the service immediately to test it:

sudo systemctl start timer.service

Your timer application should appear on the screen. If it doesn't, you can check its status for errors with sudo systemctl status timer.service.

Now, every time you reboot your Raspberry Pi, your timer application will launch automatically once the desktop loads.