import tkinter as tk
from tkinter import font
import atexit

# Attempt to import the GPIO library, with a fallback for non-Pi systems
try:
    import RPi.GPIO as GPIO
    IS_PI = True
except (ImportError, RuntimeError):
    IS_PI = False
    print("WARNING: RPi.GPIO library not found. GPIO controls will be disabled.")
    print("This is normal if you are not running on a Raspberry Pi.")

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
        # You can change these to any other valid GPIO pins
        self.START_STOP_PIN = 17  # Pin for Start/Stop
        self.RESET_PIN = 27       # Pin for Reset
        
        # --- General Configuration ---
        self.show_days = False
        self.bg_color = '#000000'
        self.fg_color = '#FFFFFF'
        self.quit_fg_color = '#FF0000'

        # Configure the window
        self.root.attributes('-fullscreen', True) 
        self.root.configure(bg=self.bg_color, cursor='none')

        # State variables
        self.running = False
        self.seconds = 0
        self.hide_job = None

        # Style configuration
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
            # Register the GPIO cleanup function to be called on exit
            atexit.register(self.cleanup_gpio)

    def setup_ui(self):
        """Creates and places all the UI widgets."""
        time_display_frame = tk.Frame(self.root, bg=self.bg_color)
        time_display_frame.pack(expand=True)
        
        self.days_label = tk.Label(
            time_display_frame, font=self.days_font, fg=self.fg_color, bg=self.bg_color
        )

        self.time_label = tk.Label(
            time_display_frame, text="00:00:00", font=self.time_font, 
            fg=self.fg_color, bg=self.bg_color
        )
        self.time_label.pack()

        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.pack(fill='x', side='bottom', pady=50)

        self.start_button = tk.Button(
            self.button_frame, text="Start", font=self.button_font,
            command=self.toggle_start_stop, bg='#28a745', fg=self.fg_color,
            activebackground='#218838', activeforeground=self.fg_color, bd=0, padx=20, pady=10
        )
        self.start_button.pack(side='left', expand=True, fill='x', padx=20)
        
        self.reset_button = tk.Button(
            self.button_frame, text="Reset", font=self.button_font,
            command=self.reset, bg='#dc3545', fg=self.fg_color,
            activebackground='#c82333', activeforeground=self.fg_color, bd=0, padx=20, pady=10
        )
        self.reset_button.pack(side='right', expand=True, fill='x', padx=20)
        
        self.quit_button = tk.Button(
            self.root, text="X", command=self.root.destroy, bg=self.bg_color,
            fg=self.quit_fg_color, font=("Helvetica", 20), bd=0, relief="flat"
        )
        self.quit_button.place(x=10, y=10)

    def setup_gpio(self):
        """Sets up the GPIO pins for input with pull-down resistors."""
        print(f"Setting up GPIO pins: Start/Stop={self.START_STOP_PIN}, Reset={self.RESET_PIN}")
        GPIO.setmode(GPIO.BCM) # Use Broadcom pin-numbering scheme

        # Setup pins as input with a pull-down resistor.
        # This means the pin is LOW by default and goes HIGH when a button connects it to 3.3V.
        GPIO.setup(self.START_STOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.RESET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Add event detection for a rising edge (LOW to HIGH)
        # bouncetime helps prevent multiple triggers from one button press
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
        """Callback function for the start/stop GPIO pin."""
        print(f"GPIO Start/Stop event detected on channel {channel}.")
        self.toggle_start_stop()

    def gpio_reset_callback(self, channel):
        """Callback function for the reset GPIO pin."""
        print(f"GPIO Reset event detected on channel {channel}.")
        self.reset()

    def cleanup_gpio(self):
        """Called on script exit to clean up GPIO resources."""
        print("Cleaning up GPIO...")
        GPIO.cleanup()

    def schedule_hide(self):
        self.hide_job = self.root.after(3000, self.hide_controls)

    def hide_controls(self):
        self.button_frame.pack_forget()
        self.quit_button.place_forget()
        self.root.config(cursor='none')

    def handle_mouse_move(self, event=None):
        if self.hide_job:
            self.root.after_cancel(self.hide_job)
            self.hide_job = None
        
        self.root.config(cursor='')
        if not self.button_frame.winfo_ismapped():
            self.button_frame.pack(fill='x', side='bottom', pady=50)
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
                    self.days_label.config(text=days_string)
                    if not self.days_label.winfo_ismapped():
                        self.days_label.pack(before=self.time_label)
            else:
                hours = self.seconds // 3600
            
            minutes = (self.seconds % 3600) // 60
            secs = self.seconds % 60
            
            time_string = f"{hours:02d}:{minutes:02d}:{secs:02d}"
            self.time_label.config(text=time_string)
            
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
        self.days_label.pack_forget()
        self.time_label.config(text="00:00:00")
        self.start_button.config(text="Start", bg='#28a745', activebackground='#218838')


if __name__ == "__main__":
    main_window = tk.Tk()
    app = StopwatchApp(main_window)
    main_window.mainloop()
