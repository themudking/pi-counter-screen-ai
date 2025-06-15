import tkinter as tk
from tkinter import font

class StopwatchApp:
    """
    A simple stopwatch application built with tkinter, suitable for a Raspberry Pi.
    This version includes a day counter and controls that hide on inactivity.
    """
    def __init__(self, root):
        """
        Initialize the application.
        
        Args:
            root (tk.Tk): The main tkinter window.
        """
        self.root = root
        self.root.title("Raspberry Pi Timer")
        
        # --- Configuration ---
        # Set to True to show days on a separate line after 24 hours.
        # Set to False to let the hours count up indefinitely (e.g., 25:00:00).
        self.show_days = False

        # Color Configuration
        self.bg_color = '#000000' # Black background
        self.fg_color = '#FFFFFF' # White text
        self.quit_fg_color = '#FF0000' # Red for the quit button text

        # Configure the window
        self.root.attributes('-fullscreen', True) 
        self.root.configure(bg=self.bg_color, cursor='none') # Hide cursor by default

        # State variables
        self.running = False
        self.seconds = 0
        self.hide_job = None # To store the 'after' job ID

        # Style configuration
        self.days_font = font.Font(family='Helvetica', size=80, weight='bold')
        self.time_font = font.Font(family='Helvetica', size=220, weight='bold')
        self.button_font = font.Font(family='Helvetica', size=48)

        # Main frame to hold the time and day labels for centering
        time_display_frame = tk.Frame(self.root, bg=self.bg_color)
        time_display_frame.pack(expand=True)
        
        # Day display label - created but not displayed until needed
        self.days_label = tk.Label(
            time_display_frame,
            font=self.days_font,
            fg=self.fg_color,
            bg=self.bg_color
        )
        # Note: The label is not packed here. It will be packed in update_time().

        # Time display label (HH:MM:SS)
        self.time_label = tk.Label(
            time_display_frame, 
            text="00:00:00", 
            font=self.time_font, 
            fg=self.fg_color, 
            bg=self.bg_color
        )
        self.time_label.pack()

        # Frame to hold the control buttons
        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.pack(fill='x', side='bottom', pady=50)

        # Start/Stop Button
        self.start_button = tk.Button(
            self.button_frame, 
            text="Start", 
            font=self.button_font,
            command=self.toggle_start_stop,
            bg='#28a745', # Green
            fg=self.fg_color,
            activebackground='#218838',
            activeforeground=self.fg_color,
            bd=0,
            padx=20,
            pady=10
        )
        self.start_button.pack(side='left', expand=True, fill='x', padx=20)
        
        # Reset Button
        self.reset_button = tk.Button(
            self.button_frame, 
            text="Reset", 
            font=self.button_font,
            command=self.reset,
            bg='#dc3545', # Red
            fg=self.fg_color,
            activebackground='#c82333',
            activeforeground=self.fg_color,
            bd=0,
            padx=20,
            pady=10
        )
        self.reset_button.pack(side='right', expand=True, fill='x', padx=20)
        
        # Add a quit button that will also hide/show
        self.quit_button = tk.Button(
            self.root,
            text="X",
            command=self.root.destroy,
            bg=self.bg_color,
            fg=self.quit_fg_color,
            font=("Helvetica", 20),
            bd=0,
            relief="flat"
        )
        self.quit_button.place(x=10, y=10)

        # Bind mouse movement to show controls and schedule them to hide
        self.root.bind('<Motion>', self.handle_mouse_move)
        # Initially schedule the controls to hide
        self.schedule_hide()


    def schedule_hide(self):
        """Schedules the controls and cursor to be hidden after a delay."""
        self.hide_job = self.root.after(3000, self.hide_controls)

    def hide_controls(self):
        """Hides the button frame, quit button, and the mouse cursor."""
        self.button_frame.pack_forget()
        self.quit_button.place_forget()
        self.root.config(cursor='none')

    def handle_mouse_move(self, event=None):
        """Shows the controls and cursor and schedules them to be hidden again."""
        # Cancel any pending hide job
        if self.hide_job:
            self.root.after_cancel(self.hide_job)
            self.hide_job = None
        
        # Show the cursor
        self.root.config(cursor='')

        # Show the button frame if it's hidden
        if not self.button_frame.winfo_ismapped():
            self.button_frame.pack(fill='x', side='bottom', pady=50)

        # Show the quit button if it's hidden
        if not self.quit_button.winfo_ismapped():
            self.quit_button.place(x=10, y=10)
        
        # Schedule to hide them again
        self.schedule_hide()


    def update_time(self):
        """
        Increments the timer by one second and updates the display labels.
        Schedules itself to run again after 1 second if the timer is running.
        """
        if self.running:
            self.seconds += 1
            
            if self.show_days:
                # Logic to show days on a separate line
                days = self.seconds // 86400
                hours = (self.seconds % 86400) // 3600
                if days > 0:
                    days_string = f"{days} day{'s' if days != 1 else ''}"
                    self.days_label.config(text=days_string)
                    if not self.days_label.winfo_ismapped():
                        self.days_label.pack(before=self.time_label)
            else:
                # Logic to let hours accumulate
                hours = self.seconds // 3600
            
            minutes = (self.seconds % 3600) // 60
            secs = self.seconds % 60
            
            time_string = f"{hours:02d}:{minutes:02d}:{secs:02d}"
            self.time_label.config(text=time_string)
            
            self.root.after(1000, self.update_time)

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
        self.days_label.pack_forget() # Hide the days label regardless
        self.time_label.config(text="00:00:00")
        self.start_button.config(text="Start", bg='#28a745', activebackground='#218838')


if __name__ == "__main__":
    # Create the main window
    main_window = tk.Tk()
    
    # Instantiate and run the application
    app = StopwatchApp(main_window)
    main_window.mainloop()
