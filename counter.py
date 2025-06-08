import tkinter as tk
from tkinter import font
import os

class StopwatchApp:
    """
    A simple stopwatch application built with tkinter, suitable for a Raspberry Pi.
    This version includes a day counter on a separate line that only appears when days > 0.
    Now also displays images sequentially.
    """
    def __init__(self, root):
        """
        Initialize the application.
        
        Args:
            root (tk.Tk): The main tkinter window.
        """
        self.root = root
        self.root.title("Raspberry Pi Timer")
        # Configure the window to be full screen for better visibility on a Pi display
        # You can comment this out for development on a desktop
        self.root.attributes('-fullscreen', True) 
        self.root.configure(bg='black')

        # State variables
        self.running = False
        self.seconds = 0

        # Style configuration
        self.days_font = font.Font(family='Helvetica', size=80, weight='bold')
        self.time_font = font.Font(family='Helvetica', size=220, weight='bold')
        self.button_font = font.Font(family='Helvetica', size=48)

        # Main frame to hold the time and day labels for centering
        time_display_frame = tk.Frame(self.root, bg='black')
        time_display_frame.pack(expand=True)
        
        # Day display label - created but not displayed until needed
        self.days_label = tk.Label(
            time_display_frame,
            font=self.days_font,
            fg='white',
            bg='black'
        )
        # Note: The label is not packed here. It will be packed in update_time().

        # Time display label (HH:MM:SS)
        self.time_label = tk.Label(
            time_display_frame, 
            text="00:00:00", 
            font=self.time_font, 
            fg='white', 
            bg='black'
        )
        self.time_label.pack()

        # Frame to hold the control buttons
        button_frame = tk.Frame(self.root, bg='black')
        button_frame.pack(fill='x', side='bottom', pady=50)

        # Start/Stop Button
        self.start_button = tk.Button(
            button_frame, 
            text="Start", 
            font=self.button_font,
            command=self.toggle_start_stop,
            bg='#28a745', # Green
            fg='white',
            activebackground='#218838',
            activeforeground='white',
            bd=0,
            padx=20,
            pady=10
        )
        self.start_button.pack(side='left', expand=True, fill='x', padx=20)
        
        # Reset Button
        self.reset_button = tk.Button(
            button_frame, 
            text="Reset", 
            font=self.button_font,
            command=self.reset,
            bg='#dc3545', # Red
            fg='white',
            activebackground='#c82333',
            activeforeground='white',
            bd=0,
            padx=20,
            pady=10
        )
        self.reset_button.pack(side='right', expand=True, fill='x', padx=20)
        
        # Add a quit button to exit fullscreen mode easily
        self.quit_button = tk.Button(
            self.root,
            text="X",
            command=self.root.destroy,
            bg="black",
            fg="red",
            font=("Helvetica", 20),
            bd=0,
            relief="flat"
        )
        self.quit_button.place(x=10, y=10)

        self.image_folder = "img"  # Define the image folder path
        self.image_paths = [] # List to store paths of images in the folder
        self.current_image_index = 0


    def update_time(self):
        """
        Increments the timer by one second and updates the display labels.
        Schedules itself to run again after 1 second if the timer is running.
        """
        if self.running:
            self.seconds += 1
            # Calculate days, hours, minutes, seconds
            days = self.seconds // 86400
            hours = (self.seconds % 86400) // 3600
            minutes = (self.seconds % 3600) // 60
            secs = self.seconds % 60
            
            # Conditionally show and update the days label
            if days > 0:
                days_string = f"{days} day{'s' if days != 1 else ''}"
                self.days_label.config(text=days_string)
                # If the label is not visible, pack it above the time label
                if not self.days_label.winfo_ismapped():
                    self.days_label.pack(before=self.time_label)

            time_string = f"{hours:02d}:{minutes:02d}:{secs:02d}"
            self.time_label.config(text=time_string)
            
            # Schedule the next update
            self.root.after(1000, self.update_time)

            # Update image display
            if self.current_image_index < len(self.image_paths):
                image_path = self.image_paths[self.current_image_index]
                try:
                    img = tk.PhotoImage(file=image_path)
                    self.image_label.config(image=img)  # Update the image label
                    self.image_label.image = img # Keep a reference!
                    self.current_image_index += 1
                except Exception as e:
                    print(f"Error loading image {image_path}: {e}")

    def toggle_start_stop(self):
        """
        Toggles the running state of the stopwatch.
        """
        if self.running:
            # If it's running, stop it
            self.running = False
            self.start_button.config(text="Start", bg='#28a745', activebackground='#218838')
        else:
            # If it's stopped, start it
            self.running = True
            self.start_button.config(text="Stop", bg='#007bff', activebackground='#0069d9') # Blue for stop
            # Start the update loop
            self.update_time()

    def reset(self):
        """
        Stops the timer and resets the counter and displays to zero.
        """
        self.running = False
        self.seconds = 0
        self.days_label.pack_forget() # Hide the days label
        self.time_label.config(text="00:00:00")
        self.start_button.config(text="Start", bg='#28a745', activebackground='#218838')
        self.current_image_index = 0  # Reset image index
        self.time_label.config(text="00:00:00") # Reset time display

    def load_images(self):
        """Loads all images from the specified folder."""
        try:
            for filename in os.listdir(self.image_folder):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check for common image extensions
                    filepath = os.path.join(self.image_folder, filename)
                    self.image_paths.append(filepath)
        except FileNotFoundError:
            print(f"Error: Image folder '{self.image_folder}' not found.")
        except Exception as e:
            print(f"An error occurred while loading images: {e}")

if __name__ == "__main__":
    # Create the main window
    main_window = tk.Tk()
    
    # Instantiate and run the application
    app = StopwatchApp(main_window)
    main_window.mainloop()
