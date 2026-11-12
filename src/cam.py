import serial
import tkinter as tk
from PIL import Image, ImageTk
import cv2
 
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageEnhance, ImageOps, ImageFilter, ImageSequence
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageEnhance, ImageOps, ImageFilter
from tkinter import Tk, Label, Button
import cv2
import serial
import time
from utils import * 
import numpy as np



# Global variables
ser = None  # Serial port object
camera = None  # Camera object
window = None  # GUI window object
#labels=None
#model=None
#image_labe2=None

# Create GUI window
window = tk.Tk()
window.title("Green Wave Project - Waste Segregation System")
window.geometry("500x430")

# Create a label to display the Project Title
image_labe_title = tk.Label(window, text="Green Wave Project - Waste Segregation System", font=("Arial", 15), foreground="green")
image_labe_title.pack()

# Create a label to display the Student Name
image_labe_name = tk.Label(window, text="Avika Gupta, YBIS Singapore", font=("Arial", 12), foreground="black")
image_labe_name.pack()

# Create a label to display the image
image_label = tk.Label(window)
image_label.pack()

# Create a label to display the class
image_labe2 = tk.Label(window, text="Label for result", font=("Arial", 13), foreground="green")
image_labe2.pack()

# Create a label to display the  Reccylable/Non-Cyclabe
sub_label3 = tk.Label(window, text="Label for Reccylable/Non-Cyclabe", font=("Arial", 14), foreground="blue")
sub_label3.pack()
 


def load_moel_data():
    #labels = gen_labels() cardboard electronics glass metal organicwaste plastic
    global labels
    labels= {0: 'cardboard', 1: 'electronics', 2: 'glass', 3: 'metal', 4: 'organicwaste', 5: 'plastic'}
    print(labels)

    print("model loading...")
    global model
    model= model_arc()
    model.load_weights("model.h5")
    print("loading done..")

def initialize_serial_port():
    global ser
    try:
        ser = serial.Serial('COM5', 9600)  # Replace 'COM1' with your actual serial port and baud rate
        #ser = serial.Serial('/dev/ttyUSB0', 9600)  # Replace '/dev/ttyUSB0' with your actual serial port and baud rate
        print("Serial port connected successfully.")
    except serial.SerialException as e:
        print("Serial port error:", e)
        window.after(1000, initialize_serial_port)  # Retry after 1 second

def initialize_camera():
    global camera
    try:
        camera = cv2.VideoCapture(0)  # Replace 0 with the appropriate camera index if you have multiple cameras
        print("Camera connected successfully.")
    except cv2.error as e:
        print("Camera error:", e)
        window.after(1000, initialize_camera)  # Retry after 1 second

def capture_image():
    if camera is None:
        print("Camera not initialized.")
        return

    _, frame = camera.read()  # Capture a frame from the camera
    cv2.imwrite("captured_image.jpg", frame)  # Save the image to a file
    process_image("captured_image.jpg")  # Process the captured image
    display_image("processed_image.jpg")  # Display the processed image on the GUI
   

def process_image(image_path):
    # Perform image processing on the captured image
    # Replace this with your actual image processing code
    processed_image = cv2.imread(image_path)
    # Example: Convert the image to grayscale
    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("processed_image.jpg", processed_image)  # Save the processed image to a file

def display_image(image_path):
    # Open the image file and resize it
    image = Image.open(image_path)
    image = image.resize((300, 300), Image.Resampling.LANCZOS)

    # Convert the image to Tkinter-compatible format
    photo = ImageTk.PhotoImage(image)

    # Update the label with the new image
    image_label.configure(image=photo)
    image_label.image = photo

    image = Image.open("captured_image.jpg")
    print('image read for prediction')
    img = preprocess(image)
    prediction = model.predict(img[np.newaxis, ...])
    probability = np.max(prediction[0], axis=-1)
    rounded_probability = round(probability, 2)  # Round the probability to 2 decimal places
    class_index = np.argmax(prediction[0], axis=-1)
    predicted_class = labels[class_index]
    print("Classified: {}, Probability: {:.2f}".format(predicted_class, rounded_probability))    
    image_labe2.config(text="Classified: {}, Probability: {:.2f} %".format(predicted_class, rounded_probability*100))

    # here logic for check the probability of class 
    if(rounded_probability>=0.30): 
        if predicted_class == "electronics":
            recycling_status = "Non-Recyclable"
            send_serial_command("2")  # Send a command back to the serial port
        else:
            recycling_status = "Recyclable"            
            send_serial_command("1")  # Send a command back to the serial port
        print("Class: {}, Recycling Status: {}".format(predicted_class, recycling_status))
        sub_label3.config(text="Recycling Status: {}".format(recycling_status))
    else:
        recycling_status = "Unknown"
        sub_label3.config(text="Recycling Status: {}".format(recycling_status))
        send_serial_command("3")
    
    
    
    

def send_serial_command(command):
    if ser is None:
        print("Serial port not initialized.")
        return

    try:
        ser.write(command.encode())  # Send the command to the serial port
        print("Serial command sent:", command)
    except serial.SerialException as e:
        print("Serial port error:", e)
        window.after(1000, initialize_serial_port)  # Retry after 1 second

def read_serial():
    if ser is None:
        print("Serial port not initialized.")
        return

    try:
        data = ser.readline().decode('latin-1').strip()  # Read a line from the serial port and decode it as Latin-1
        if data == "1":
            capture_image()
        
    except serial.SerialException as e:
        print("Serial port error:", e)
        window.after(1000, initialize_serial_port)  # Retry after 1 second

    # Schedule the next read after 100 milliseconds
    window.after(100, read_serial)
    

def writeBrand(resized_image):
    # Draw your name on the resized image
    draw = ImageDraw.Draw(resized_image)
    font = ImageFont.truetype("arial.ttf", 16)  # Specify the font and font size
    name = "Name: Avika Gupta, YBIS Singapore"
    text_bbox = draw.textbbox((0, 0), name, font=font)
    x = resized_image.width - text_bbox[2] - 10  # Position the name on the top right corner
    y = 10
    draw.text((x, y), name, fill=(255, 255, 255), font=font)  # Add the name to the image
    
    
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

        #this function write brand info on image 
        #writeBrand(resized_image)
    
        photo = ImageTk.PhotoImage(resized_image)

        # Update the label with the new frame
        image_label.configure(image=photo)
        image_label.image = photo
    except cv2.error as e:
        print("Camera error:", e)
        window.after(1000, initialize_camera)  # Retry after 1 second

    # Schedule the next frame update after 10 milliseconds
    window.after(10, update_video_feed)

# Initialize serial port and camera
initialize_serial_port()
initialize_camera()
load_moel_data()
# Start reading from the serial port
read_serial()
 
# Start the video feed
update_video_feed()

# Start the GUI event loop
window.mainloop()

# Release resources
if ser is not None:
    ser.close()
if camera is not None:
    camera.release()
cv2.destroyAllWindows()
