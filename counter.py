import tkinter as tk
import time

# Configuration
window_title = "Time Counter"
label_text = "Count: 0"
update_interval = 1  # Seconds initially

def update_count():
    global counter, label
    counter += 1

    if counter >= 60: # Every minute
        counter %= 60
        label.config(text=f"{counter // 60:02d}:" + f"{counter % 60:02d}")
    elif counter >= 3600: # Every hour
        counter %= 3600
        label.config(text=f"{counter // 3600:04d}:" + f"{counter % 3600:04d}")
    elif counter >= 86400: # Every day
        counter %= 86400
        label.config(text=f"{counter // 86400:03d}")

    else:
        label.config(text=f"{label_text} {counter}")

    root.after(update_interval * 1000)


root = tk.Tk()
root.title(window_title)

counter = 0
label = tk.Label(root, text=label_text, font=("Helvetica", 24))
label.pack(pady=20)

update_count()  # Start the counter update loop

root.mainloop()
