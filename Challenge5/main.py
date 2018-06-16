#pickle serializacja obiektow pickle.dump do pliku
from flask import Flask, jsonify, request, make_response, abort
app = Flask(__name__)

from PIL import Image

from sklearn import datasets
from sklearn import metrics
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier as classifier

from io import BytesIO

import os
import sys
import time
import pickle
import logging

from aux_io import file_to_image
from aux_img import get_img_array, get_resized_image, normalize_image
import numpy as np

print('Highest pickle protocol=' + str(pickle.HIGHEST_PROTOCOL))

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

try:
    print('Initializing model...')
    model = pickle.load(open(os.path.join(__location__, "model.pickle"), "rb"))
    print('Done')
except:
    print('Failed to load the model file: ', sys.exc_info()[0])
    raise

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/predict', methods=['POST'])
def predict():
    print(request)
    
    file = request.files['file']
    if not file:
        abort(400)
    
    img = file_to_image(file)
    img = get_resized_image(img, 128)
    img = normalize_image(img)
    
    arr = get_img_array(img).reshape(-1)

    data = []
    data.append(arr)

    prediction = model.predict(np.asarray(data))

    return jsonify({ 
        "result": "Ok",
        "prediction": str(prediction)
        })

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')