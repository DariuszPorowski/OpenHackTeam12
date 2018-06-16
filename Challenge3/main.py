import os
import numpy as np

basePath = "/home/jupyter/notebooks"
dataPath = basePath + '/challenge1/data'
validationPath = basePath + '/challenge1/validation'

def get_subdirs(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

def get_files(dir):
    return np.asarray(os.listdir(dir))

for dir in get_subdirs(dataPath):
    print(dir)


# ===


from PIL import Image
import numpy as np

# Get the PIL Image
def get_img(path):
    return Image.open(path);

def get_img_path(basePath, imgType, imgName):
    return basePath + '/' + imgType + '/' + imgName

# Convert the PIL Image to numpy array
def get_img_array(img):
    return np.array(img)


# ===


from sklearn import datasets
from sklearn import metrics
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier as classifier
import pickle

model = classifier()
data = []
target = []

for dir in get_subdirs(dataPath):
    files = get_files(dataPath + '/' + dir)
      
    for file in files:
        img = get_img(get_img_path(dataPath, dir, file))
        arr = get_img_array(img)
        #print(arr.shape)
        data.append(arr.reshape(-1))
        target.append(dir)
    
    print('Fitting ' + str(files.size) + ' images of class: ' + dir)
    
data = np.asarray(data)
target = np.asarray(target).reshape(-1)

print('=== === === === ===')
print('Data shape is: ' + str(data.shape))
print('Target shape is: ' + str(target.shape))
    

model.fit(data, target)
print('Model ready!')

with open('model.pickle', 'wb') as handle:
    pickle.dump(model, handle, protocol=2)

#print("Confusion matrix:\n%s" % metrics.confusion_matrix(data, model))


validationData = []
expectedLabels = []

for dir in get_subdirs(validationPath):
    files = get_files(validationPath + '/' + dir)
    
    for file in files:
        img = get_img(get_img_path(validationPath, dir, file))
        arr = get_img_array(img)
        validationData.append(arr.reshape(-1))
        expectedLabels.append(dir)
        
validationData = np.asarray(validationData)
expectedLabels = np.asarray(expectedLabels)

prediction = model.predict(validationData)
#print('Prediction: ' + str(prediction))

print('=== REPORT ===')
#print("Classification report for classifier %s:\n%s\n"
#      % (classifier, metrics.classification_report(validationData, prediction)))
print('Validation data shape is: ' + str(validationData.shape))
print('Y_Test shape is: ' + str(expectedLabels.shape))
print('Prediction shape is: ' + str(prediction.shape))

# confusion_matrix(y_test, predictions)
print("Accuracy Score:\n%s" % accuracy_score(expectedLabels, prediction))

#print(prediction)
# DT
# make predictions
#expected = dataset.target
#predicted = model.predict(dataset.data)
# summarize the fit of the model
#print(metrics.classification_report(expected, predicted))
#print(metrics.confusion_matrix(expected, predicted))