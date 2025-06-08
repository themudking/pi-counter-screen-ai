import tkinter as tk
import time

# Configuration
window_title = "Counter App"
label_text = "Count: 0"
update_interval = 1  # seconds

def update_count():
    global counter, label
    counter += 1
    label.config(text=f"{label_text} {counter}")
    root.after(update_interval * 200) # Schedule the next update


root = tk.Tk()
root.title(window_title)

counter = 0
label = tk.Label(root, text=label_text, font=("Helvetica", 24))
label.pack(pady=20)

update_count()  # Start the counter update loop

root.mainloop()
