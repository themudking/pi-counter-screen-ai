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

[Unit] Section:

Description: A brief description of your service.

After=graphical.target: This is very important. It ensures your script only runs after the Raspberry Pi's graphical desktop environment has finished loading.

[Service] Section:

User=pi: Runs the script as the standard pi user.

Environment=DISPLAY=:0: This is the crucial part for any GUI application. It tells your script which display to connect to.

ExecStart=/usr/bin/python3 /home/pi/pi-counter-screen-ai/counter.py: The full command to execute your application. It uses the absolute paths for both the Python interpreter and your script.

Restart=always: If your application crashes for any reason, systemd will automatically try to restart it.

[Install] Section:

WantedBy=graphical.target: This enables the service to be started as part of the graphical boot process.

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