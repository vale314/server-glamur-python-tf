import os
from keras.utils import np_utils 
import matplotlib.pyplot as plt
from tensorflow import keras
import tensorflow as tf
import numpy as np
import random
from PIL import Image 
import PIL.ImageOps 

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
from urllib.parse import urlparse, parse_qs
import uuid

HOST = "137.184.150.122"
PORT = 9999

class NeuralHTTP(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # print (self.path)
        query = urlparse(self.path).query
        if(not query.startswith("url")):
            data1 = {}
            data1["prediction"] = str(-1)

            json_to_pass1 = json.dumps(data1)
            self.wfile.write(json_to_pass1.encode('utf-8'))
            return

        query_components = dict(qc.split("=") for qc in query.split("&"))
        
        urlImage = query_components["url"]

        filename = str(uuid.uuid4().hex+".jpg")

        urllib.request.urlretrieve(urlImage, filename)
        aux = function_hola("./" + filename)

        if os.path.exists("./" + filename):
            os.remove("./" + filename)
        else:
            print("The file does not exist") 

        data = {}
        data["prediction"] = str(aux)

        json_to_pass = json.dumps(data)
        self.wfile.write(json_to_pass.encode('utf-8'))

def function_hola(image_name):
    # Recreate the exact same model, including its weights and the optimizer
    model = tf.keras.models.load_model('name.h5')

    #Show the model architecture
    #model.summary()
    
    image_file = Image.open(image_name) # open colour image
    image_file = image_file.convert('1') # convert image to black and white

    filename = str(uuid.uuid4().hex+".jpg")

    image_file.save("./" + filename)

    image = Image.open("./" + filename)
    image_file = PIL.ImageOps.invert(image)
    image_file.save("./" + filename)

    painting=plt.imread("./" + filename)
    datas = painting / 255.0

    arr = np.array([datas, datas])
    pre = model.predict(arr)

    #print(pre)
    prediction_digits = np.argmax(pre, axis=1)
    if os.path.exists("./" + filename):
        os.remove("./" + filename)
    else:
        print("The file does not exist") 

    #print (prediction_digits[0])

    return prediction_digits[0]

server = HTTPServer((HOST, PORT), NeuralHTTP)
print ("running")
server .serve_forever()
server.server_close()
