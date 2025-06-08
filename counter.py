import RPi.GPIO as GPIO  # Import the GPIO library
import tkinter as tk # Import tkinter for GUI elements (if needed)
import time
import os

# Configuration - Adjust these to your needs
SCREEN_WIDTH = 160 # Example width, adjust based on your screen
SCREEN_HEIGHT = 128 # Example height, adjust based on your screen
IMAGE_FOLDER = "img"
IMAGE_ROTATE_INTERVAL = 300  # Rotate every 300 seconds (5 minutes)

# Initialize GPIO pins - Replace with your actual pin numbers
BUTTON_START_PIN = 17
BUTTON_RESET_PIN = 27


root = tk.Tk()
root.title("Image Display") # Set a title for the window
root.geometry("600x400") # Set an initial size for the window

def setup_gpio():
    GPIO.setmode(GPIO.BCM) # Use BCM pin numbering
    GPIO.setup(BUTTON_START_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_RESET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def get_image_path():
    files = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]
    if files:
        return os.path.join(IMAGE_FOLDER, max(files)) # Get the highest numbered file
    else:
        return None

def display_counter():
    # This is a placeholder - Replace with your actual screen drawing code
    print("Counter Display:", time.strftime("%H:%M"))


def main():
    setup_gpio()

    start_button_pressed = False # Flag to track start button state
    counter_running = False

    try:
        while True:
            # Check for button presses
            if not GPIO.input(BUTTON_START_PIN):
                print("Start Button Pressed")
                if not counter_running:
                    start_button_pressed = True
                    counter_running = True
                    time.sleep(1) # Debounce the start button

            if GPIO.input(BUTTON_RESET_PIN):
                print("Reset Button Pressed")
                counter_running = False
                # Reset counter to 00:00:00 here (implementation needed)

            if counter_running:
                display_counter()
                time.sleep(1) # Update every second

            # Image rotation - run this periodically
            time.sleep(IMAGE_ROTATE_INTERVAL)
            image_path = get_image_path()
            if image_path:
                print("Rotating Image:", image_path)
                # Add code here to display the image on your screen


    except KeyboardInterrupt:
        print("Program stopped")
    finally:
        GPIO.cleanup() # Clean up GPIO pins on exit

if __name__ == "__main__":
    main()
    
root.mainloop()