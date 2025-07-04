import tkinter as tk
from tkinter import font
import atexit
import os

# Attempt to import the GPIO library, with a fallback for non-Pi systems
try:
    import RPi.GPIO as GPIO
    IS_PI = True
except (ImportError, RuntimeError):
    IS_PI = False
    print("WARNING: RPi.GPIO library not found. GPIO controls will be disabled.")
    print("This is normal if you are not running on a Raspberry Pi.")

# Attempt to import the Pillow library for image handling
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("WARNING: Pillow library not found. Image will not be displayed.")

class StopwatchApp:
    """
    A simple stopwatch application with tkinter GUI and GPIO controls.
    """
    def __init__(self, root):
        """
        Initialize the application.
        
        Args:
            root (tk.Tk): The main tkinter window.
        """
        self.root = root
        self.root.title("Raspberry Pi Timer")

        # --- GPIO Pin Configuration ---
        self.START_STOP_PIN = 17
        self.RESET_PIN = 27
        
        # --- General Configuration ---
        self.show_days = False
        self.bg_color = '#000000'
        self.fg_color = '#FFFFFF'
        self.quit_fg_color = '#FF0000'
        
        # --- Image Configuration ---
        # Create a folder named 'images' in the same directory as this script
        # and place your background images inside it.
        self.image_folder = "images"
        self.image_paths = []
        if os.path.isdir(self.image_folder):
            self.image_paths = sorted([
                os.path.join(self.image_folder, f) for f in os.listdir(self.image_folder)
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
            ])
        
        # --- Force full screen geometry ---
        # This is more robust than relying solely on the '-fullscreen' attribute.
        # It ensures the window takes up the entire screen space from the start.
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Now set the fullscreen attribute to remove window decorations (like the title bar)
        self.root.attributes('-fullscreen', True) 
        self.root.configure(bg=self.bg_color, cursor='none')

        # State variables
        self.running = False
        self.seconds = 0
        self.hide_job = None
        self.photo = None # To hold a reference to the background image
        self.current_image_index = 0
        self.background_image_id = None

        # Style configuration
        self.title_font = font.Font(family='Helvetica', size=60, weight='bold')
        self.days_font = font.Font(family='Helvetica', size=80, weight='bold')
        self.time_font = font.Font(family='Helvetica', size=220, weight='bold')
        self.button_font = font.Font(family='Helvetica', size=48)

        # UI Widget Setup
        self.setup_ui()

        # Bind mouse movement for UI control visibility
        self.root.bind('<Motion>', self.handle_mouse_move)
        self.schedule_hide()

        # Setup GPIO if running on a Raspberry Pi
        if IS_PI:
            self.setup_gpio()
            atexit.register(self.cleanup_gpio)

    def setup_ui(self):
        """Creates and places all the UI widgets with a full-screen background image."""
        # Create a canvas that will fill the screen
        self.canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Create a placeholder for the background image on the canvas
        self.background_image_id = self.canvas.create_image(0, 0, anchor="nw")
        
        # Start the background image rotation
        self.rotate_background_image()

        # --- Create text items on the canvas ---
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.canvas.create_text(
            screen_width / 2, screen_height * 0.25,
            text="50 Hour Prayer Marathon", font=self.title_font, fill=self.fg_color
        )

        self.days_text_id = self.canvas.create_text(
            screen_width / 2, screen_height * 0.45,
            text="0 days", font=self.days_font, fill=self.fg_color, state='hidden'
        )

        self.time_text_id = self.canvas.create_text(
            screen_width / 2, screen_height * 0.5,
            text="00:00:00", font=self.time_font, fill=self.fg_color, anchor='n'
        )

        # --- Place standard widgets on top of the canvas ---
        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.place(relx=0.5, rely=1.0, relwidth=1.0, y=-50, anchor='s')

        self.start_button = tk.Button(
            self.button_frame, text="Start", font=self.button_font,
            command=self.toggle_start_stop, bg='#28a745', fg=self.fg_color,
            activebackground='#218838', activeforeground=self.fg_color, bd=0, padx=20, pady=10
        )
        self.start_button.pack(side='left', expand=True, fill='x', padx=20, pady=10)
        
        self.reset_button = tk.Button(
            self.button_frame, text="Reset", font=self.button_font,
            command=self.reset, bg='#dc3545', fg=self.fg_color,
            activebackground='#c82333', activeforeground=self.fg_color, bd=0, padx=20, pady=10
        )
        self.reset_button.pack(side='right', expand=True, fill='x', padx=20, pady=10)
        
        self.quit_button = tk.Button(
            self.root, text="X", command=self.root.destroy, bg=self.bg_color,
            fg=self.quit_fg_color, font=("Helvetica", 20), bd=0, relief="flat"
        )
        self.quit_button.place(x=10, y=10)

    def rotate_background_image(self):
        """Loads the next image, sets it as the background, and schedules the next rotation."""
        if not HAS_PIL or not self.image_paths:
            print("Cannot rotate images: Pillow not installed or no images found.")
            return

        try:
            image_path = self.image_paths[self.current_image_index]
            
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            original_image = Image.open(image_path)
            resized_image = original_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            
            self.photo = ImageTk.PhotoImage(resized_image)
            self.canvas.itemconfig(self.background_image_id, image=self.photo)
            
            # Increment index for the next rotation, looping back to the start
            self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)

        except Exception as e:
            print(f"Error loading background image '{image_path}': {e}")
            # Skip to the next image on error
            self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)

        # Schedule the next rotation in 30 seconds (30000 ms)
        self.root.after(30000, self.rotate_background_image)

    def setup_gpio(self):
        """Sets up the GPIO pins for input with pull-down resistors."""
        print(f"Setting up GPIO pins: Start/Stop={self.START_STOP_PIN}, Reset={self.RESET_PIN}")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.START_STOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.RESET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(
            self.START_STOP_PIN, GPIO.RISING, 
            callback=self.gpio_toggle_callback, bouncetime=300
        )
        GPIO.add_event_detect(
            self.RESET_PIN, GPIO.RISING, 
            callback=self.gpio_reset_callback, bouncetime=300
        )
        print("GPIO event detection is now active.")

    def gpio_toggle_callback(self, channel):
        print(f"GPIO Start/Stop event detected on channel {channel}.")
        self.toggle_start_stop()

    def gpio_reset_callback(self, channel):
        print(f"GPIO Reset event detected on channel {channel}.")
        self.reset()

    def cleanup_gpio(self):
        if IS_PI:
            print("Cleaning up GPIO...")
            GPIO.cleanup()

    def schedule_hide(self):
        self.hide_job = self.root.after(3000, self.hide_controls)

    def hide_controls(self):
        self.button_frame.place_forget()
        self.quit_button.place_forget()
        self.root.config(cursor='none')

    def handle_mouse_move(self, event=None):
        if self.hide_job:
            self.root.after_cancel(self.hide_job)
            self.hide_job = None
        
        self.root.config(cursor='')
        if not self.button_frame.winfo_ismapped():
            self.button_frame.place(relx=0.5, rely=1.0, relwidth=1.0, y=-50, anchor='s')
        if not self.quit_button.winfo_ismapped():
            self.quit_button.place(x=10, y=10)
        
        self.schedule_hide()

    def update_time(self):
        if self.running:
            self.seconds += 1
            
            if self.show_days:
                days = self.seconds // 86400
                hours = (self.seconds % 86400) // 3600
                if days > 0:
                    days_string = f"{days} day{'s' if days != 1 else ''}"
                    self.canvas.itemconfig(self.days_text_id, text=days_string, state='normal')
            else:
                hours = self.seconds // 3600
            
            minutes = (self.seconds % 3600) // 60
            secs = self.seconds % 60
            
            time_string = f"{hours:02d}:{minutes:02d}:{secs:02d}"
            self.canvas.itemconfig(self.time_text_id, text=time_string)
            
            self.root.after(1000, self.update_time)

    def toggle_start_stop(self):
        if self.running:
            self.running = False
            self.start_button.config(text="Start", bg='#28a745', activebackground='#218838')
        else:
            self.running = True
            self.start_button.config(text="Stop", bg='#007bff', activebackground='#0069d9')
            self.update_time()

    def reset(self):
        self.running = False
        self.seconds = 0
        self.canvas.itemconfig(self.days_text_id, state='hidden')
        self.canvas.itemconfig(self.time_text_id, text="00:00:00")
        self.start_button.config(text="Start", bg='#28a745', activebackground='#218838')


if __name__ == "__main__":
    main_window = tk.Tk()
    app = StopwatchApp(main_window)
    main_window.mainloop()
