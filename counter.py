import tkinter as tk
import time

class Timer:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Clock")

        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.days = 0

        self.label = tk.Label(root, text=self.format_time(), font=("Helvetica", 48))
        self.label.pack(pady=50)

        self.running = False
        self.start_time = None

        start_button = tk.Button(root, text="Start", command=self.start_timer)
        start_button.pack(side=tk.LEFT, padx=10)

        #stop_button = tk.Button(root, text="Stop", command=self.stop_timer)
        #stop_button.pack(side=tk.LEFT, padx=10)

        reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        reset_button.pack(side=tk.LEFT, padx=10)

    def format_time(self):
        return f"{self.days:02}:{self.hours:02}:{self.minutes:02}:{self.seconds:02}"

    def update_timer(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            total_seconds = int(elapsed_time)

            self.days = total_seconds // (24 * 3600)
            remaining_seconds = total_seconds % (24 * 3600)

            self.hours = remaining_seconds // 3600
            remaining_seconds %= 3600

            self.minutes = remaining_seconds // 60
            self.seconds = remaining_seconds % 60

            self.label.config(text=self.format_time())
            self.root.after(1000, self.update_timer) # Update every 1000 ms (1 second)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.update_timer()

    def stop_timer(self):
        self.running = False

    def reset_timer(self):
        self.stop_timer()
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.days = 0
        self.label.config(text=self.format_time())
        self.start_time = None

if __name__ == "__main__":
    root = tk.Tk()
    timer = Timer(root)
    root.mainloop()
