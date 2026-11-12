import tkinter as tk
import cv2
import os
import time

# Global variables
capture_folder = ""  # Set the folder where images will be saved
capture_count = 1
capture_in_progress = False

# Create a function to handle capturing images
def capture_image():
    global capture_count, capture_in_progress

    if not capture_in_progress:
        capture_in_progress = True
        camera = cv2.VideoCapture(1)
        #camera.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
        #camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 384)

        # Create the capture folder if it doesn't exist
        if not os.path.exists(capture_folder):
            os.makedirs(capture_folder)

        # Start capturing images
        for i in range(30):
            ret, frame = camera.read()
            if ret:
                # Generate the file name with a serial number and folder name
                file_name = f"{capture_folder}_{capture_count:02d}.jpg"
                file_path = os.path.join(capture_folder, file_name)

                # Resize the image to 400x300
                #frame = cv2.resize(frame, (512,384))

                # Save the image
                cv2.imwrite(file_path, frame)
                print(f"Image {capture_count} captured.")

                capture_count += 1
                counter_label.config(text=f"Captured: {capture_count - 1}")

                window.update()  # Update the UI to reflect the new counter value
                time.sleep(1)  # 5-second delay between captures

        camera.release()
        capture_in_progress = False
        capture_count=1
        

# Create a Tkinter window
window = tk.Tk()
window.title("Image Capture")
window.geometry("400x300")

# Create a function to handle button click event
def start_capture():
    global capture_folder
    capture_folder = folder_entry.get()
    capture_image()

# Create UI elements
folder_label = tk.Label(window, text="Folder Name:")
folder_label.pack()

folder_entry = tk.Entry(window)
folder_entry.pack()

capture_button = tk.Button(window, text="Start Capture", command=start_capture)
capture_button.pack()

counter_label = tk.Label(window, text="Captured: 0")
counter_label.pack()

# Start the Tkinter event loop
window.mainloop()
