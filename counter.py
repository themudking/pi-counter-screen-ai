import RPi.GPIO as GPIO
import tkinter as tk
import time  # Import the time module
import os

# Configuration - Adjust these to your needs
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 128
IMAGE_FOLDER = "img"
IMAGE_ROTATE_INTERVAL = 300

# Initialize GPIO pins
BUTTON_START_PIN = 17
BUTTON_RESET_PIN = 27


def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_START_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_RESET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def get_image_path():
    files = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]
    if files:
        return os.path.join(IMAGE_FOLDER, max(files))
    else:
        return None


def display_counter(screen):
    # Clear the screen (replace with your screen clearing method)
    for widget in screen.winfo_children():
        widget.destroy()

    # Draw the counter
    font_size = 16  # Adjust font size as needed
    text_x = SCREEN_WIDTH // 2
    text_y = SCREEN_HEIGHT // 2
    screen.create_text(text_x, text_y, text="00:00:00", fill="black", font=("Arial", font_size))


def main():
    setup_gpio()

    # Create the Tkinter window
    window = tk.Tk()
    window.title("Image and Counter Display")
    window.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")  # Set window size
    window.configure(bg="#FFFFFF")  # Set background color

    # Create a canvas to draw on
    canvas = tk.Canvas(window, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="#FFFFFF")
    canvas.pack()

    start_button_pressed = False
    counter_running = False

    try:
        while True:
            if not GPIO.input(BUTTON_START_PIN):
                print("Start Button Pressed")
                if not counter_running:
                    start_button_pressed = True
                    counter_running = True
                    time.sleep(1)

            if GPIO.input(BUTTON_RESET_PIN):
                print("Reset Button Pressed")
                counter_running = False
                display_counter(canvas)  # Reset the display

            if counter_running:
                display_counter(canvas)
                time.sleep(1)

            time.sleep(IMAGE_ROTATE_INTERVAL)
            image_path = get_image_path()
            if image_path:
                print("Rotating Image:", image_path)
                try:
                    # Load the image using PIL (Pillow)
                    from PIL import Image, ImageTk  # Import Pillow modules

                    img = Image.open(image_path)
                    photo = ImageTk.PhotoImage(img)

                    # Draw the image on the canvas
                    canvas.create_image(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, image=photo, anchor=tk.CENTER)  # Anchor for centering

                except Exception as e:
                    print(f"Error loading or displaying image: {e}")


    except KeyboardInterrupt:
        print("Program stopped")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()

root = tk.Tk()
root.title("Image Display") # Set a title for the window
root.geometry("600x400") # Set an initial size for the window

root.mainloop() # Start the Tkinter event loop