import tkinter as tk
import time
import os

IMAGE_FOLDER = "img"  # Or your image folder name
IMAGE_ROTATE_INTERVAL = 2 # seconds
BUTTON_START_PIN = 17
BUTTON_RESET_PIN = 18

def display_image(canvas, image_path):
    try:
        photo = tk.PhotoImage(file=os.path.join(IMAGE_FOLDER, image_path))
        photo_id = canvas.create_image(250, 250, anchor=tk.CENTER, image=photo)
        return photo_id
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def rotate_images():
    global image_index
    image_index = (image_index + 1) % len(image_names)
    display_image(canvas, image_names[image_index])


root = tk.Tk()
root.title("Image Display")
root.geometry("600x400")

canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()

image_index = 0  # Start with the first image
image_names = [f"image{i+1}.png" for i in range(5)] # Example - adjust to your images

def start_button_callback():
    global image_index
    rotate_images()

def reset_button_callback():
    global image_index
    image_index = 0
    rotate_images()


start_button = tk.Button(root, text="Start", command=start_button_callback)
start_button.pack(side=tk.LEFT)

reset_button = tk.Button(root, text="Reset", command=reset_button_callback)
reset_button.pack(side=tk.RIGHT)


# Initial image display
display_image(canvas, image_names[image_index])



root.mainloop()
