import time

# Configuration (we'll expand on these later)
background_color = "#FFFFFF" # White
image_path = "img/image1.png"

def main():
    print("Application started!")
    counter = 0
    while True:
        try:
            # Display the counter
            print(counter, end=" ")
            time.sleep(1) # Update every second

        except KeyboardInterrupt:
            print("\nApplication stopped.")
            break


if __name__ == "__main__":
    main()
