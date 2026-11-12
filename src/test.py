from utils import *
import time
import numpy as np
from PIL import Image


#labels = gen_labels()

labels= {0: 'cardboard', 1: 'electronics', 2: 'glass', 3: 'metal', 4: 'organicwaste', 5: 'plastic'}
print(labels)

print("model loading...")
model = model_arc()
model.load_weights("model.h5")
print("loading done..")

image = Image.open("modelGen/Data/Test/organicwaste/image1_apple.jpg")
img = preprocess(image)
prediction = model.predict(img[np.newaxis, ...])
print("classified: {}".format(labels[np.argmax(prediction[0], axis=-1)]))
 
