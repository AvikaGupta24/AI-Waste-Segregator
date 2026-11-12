import serial
import tkinter as tk
from PIL import Image, ImageTk
import cv2
from tkinter import messagebox
import os

from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageEnhance, ImageOps, ImageFilter, ImageSequence
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageEnhance, ImageOps, ImageFilter
from tkinter import Tk, Label, Button
import cv2
import time
from utils import *
import numpy as np

# Global variables
ser = None  # Serial port object
camera = None  # Camera object
window = None  # GUI window object
counter = 0
folder_name = ""

# Create GUI window
window = tk.Tk()
window.title("Camera Capture")
window.geometry("400x400")

# Create a label to display the image
image_label = tk.Label(window)
image_label.pack()

 

# Create a label to display the counter
counter_label = tk.Label(window, text="Counter: 0")
counter_label.pack()

def initialize_camera():
    global camera
    try:
        camera = cv2.VideoCapture(0)  # Replace 0 with the appropriate camera index if you have multiple cameras
        #camera.set(3, 512)  # Set width to 512
        #camera.set(4, 384)  # Set height to 384
        print("Camera connected successfully.")
    except cv2.error as e:
        print("Camera error:", e)
        window.after(1000, initialize_camera)  # Retry after 1 second


def capture_image():
    global counter, folder_name
    if camera is None:
        print("Camera not initialized.")
        return

    if not folder_name:
        messagebox.showerror("Error", "Please enter a folder name.")
        return

    _, frame = camera.read()  # Capture a frame from the camera
    image_path = os.path.join(folder_name, "image{}.jpg".format(counter + 1))  # Generate a new image file path
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)  # Create the folder if it doesn't exist

    cv2.imwrite(image_path, frame)  # Save the image to a file
    counter += 1  # Increase the counter
    counter_label.config(text="Counter: {}".format(counter))  # Update the counter label

    if counter == 30:
        messagebox.showinfo("Capture Complete", "Capture has done!")  # Show an alert message when counter reaches 10
        counter=0

    display_image(image_path)  # Display the processed image on the GUI


def display_image(image_path):
    # Open the image file and resize it
    image = Image.open(image_path)
    image = image.resize((300, 300), Image.Resampling.LANCZOS)

    # Convert the image to Tkinter-compatible format
    photo = ImageTk.PhotoImage(image)

    # Update the label with the new image
    image_label.configure(image=photo)
    image_label.image = photo

   

def update_video_feed():
    if camera is None:
        print("Camera not initialized.")
        return

    try:
        _, frame = camera.read()  # Capture a frame from the camera

        # Convert the frame to PIL Image format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)

        # Resize the image and convert it to Tkinter-compatible format
        resized_image = image.resize((300, 300), resample=Image.Resampling.BICUBIC)

        photo = ImageTk.PhotoImage(resized_image)

        # Update the label with the new frame
        image_label.configure(image=photo)
        image_label.image = photo
    except cv2.error as e:
        print("Camera error:", e)
        window.after(1000, initialize_camera)  # Retry after 1 second

    # Schedule the next frame update after 10 milliseconds
    window.after(10, update_video_feed)


def set_folder_name():
    global folder_name
    folder_name = folder_entry.get()


initialize_camera()


# Create a button to capture images
capture_button = tk.Button(window, text="Capture", command=capture_image)
capture_button.pack()

# Create a folder entry and button to set the folder name
folder_frame = tk.Frame(window)
folder_frame.pack()

folder_label = tk.Label(folder_frame, text="Folder Name:")
folder_label.pack(side=tk.LEFT)

folder_entry = tk.Entry(folder_frame)
folder_entry.pack(side=tk.LEFT)

set_folder_button = tk.Button(folder_frame, text="Set", command=set_folder_name)
set_folder_button.pack(side=tk.LEFT)

# Start the video feed
update_video_feed()

# Start the GUI event loop
window.mainloop()

# Release resources
if camera is not None:
    camera.release()
cv2.destroyAllWindows()
