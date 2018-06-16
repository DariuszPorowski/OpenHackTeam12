import os
import numpy as np

def get_subdirs(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

def get_files(dir):
    return np.asarray(os.listdir(dir))

for dir in get_subdirs(trainingDataPath):
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

from sklearn.model_selection import train_test_split
from PIL import Image

def get_resized_image(image, desired_size):
    #im = Image.open(im_pth)
    old_size = image.size  # old_size[0] is in (width, height) format
    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])

    im = image.resize(new_size, Image.ANTIALIAS)

    WHITE = (255, 255, 255)
    new_im = Image.new("RGB", (desired_size, desired_size), WHITE)
    new_im.paste(im, ((desired_size-new_size[0])//2, (desired_size-new_size[1])//2))
    return new_im

def normalize(arr):
    """
    Linear normalization
    http://en.wikipedia.org/wiki/Normalization_%28image_processing%29
    """
    arr = arr.astype('float')
    # Do not touch the alpha channel
    for i in range(3):
        minval = arr[...,i].min()
        maxval = arr[...,i].max()
        if minval != maxval:
            arr[...,i] -= minval
            arr[...,i] *= (255.0/(maxval-minval))
    return arr

def normalize_image(img):
    imgArr = np.array(img)
    normalizedArr = normalize(imgArr)
    return Image.fromarray(normalizedArr.astype('uint8'))
    

# ===

import os
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical
import keras

#os.environ["KERAS_BACKEND"] = "cntk"

basePath = "/home/jupyter/notebooks"
trainingDataPath = basePath + '/challenge1/data'
validationDataPath = basePath + '/challenge1/validation'
dataPath = basePath + '/challenge4'


img_target_size = (128, 128)
img_input_shape = (128, 128, 3)
conv_size = (3, 3)
conv_neurons = 64

model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3),

                 activation='relu',

                 input_shape=img_input_shape))

model.add(Conv2D(64, (3, 3), activation='relu'))

model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Dropout(0.25))

model.add(Flatten())

model.add(Dense(128, activation='relu'))

model.add(Dropout(0.5))

model.add(Dense(12, activation='softmax'))



model.compile(loss=keras.losses.categorical_crossentropy,

              optimizer=keras.optimizers.Adadelta(),

              metrics=['accuracy'])



# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1./255)

# this is a generator that will read pictures found in
# subfolers of 'data/train', and indefinitely generate
# batches of augmented image data
#train_generator = train_datagen.flow_from_directory(
#        trainingDataPath,  # this is the target directory
#        target_size = img_target_size,  # all images will be resized to 150x150
#        batch_size=batch_size,
#        class_mode='binary')  # since we use binary_crossentropy loss, we need binary labels

# this is a similar generator, for validation data
#validation_generator = test_datagen.flow_from_directory(
#        validationDataPath,
#        target_size = img_target_size,
#        batch_size=batch_size,
#        class_mode='binary')

features = []
labels = []
idx = 0
for dir in get_subdirs(dataPath):
    files = get_files(dataPath + '/' + dir)
    
    for file in files:
        img = get_img(get_img_path(dataPath, dir, file))
        arr = get_img_array(img)
        #print(arr.shape)
        features.append(arr)
        labels.append(dir)

    print('Fitting ' + str(files.size) + ' images of class[' + str(idx) + ']: ' + dir)   
    idx = idx + 1
    

features = np.asarray(features)
print('Features shape is: ' + str(features.shape))

features = features.astype('float32')
features /= 255


from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(labels)

print(list(le.classes_))

labels=le.transform(labels) 
print(labels)
#list(le.inverse_transform([2, 2, 1]))


#labels = np.array(labels)
#labels = labels.astype('float32')
#labels /= 255
#print(str(labels))
#labels = to_categorical(labels, 12)
#print(str(labels))
    # fit(self, x=None, y=None, batch_size=None, epochs=1, verbose=1, callbacks=None, validation_split=0.0, validation_data=None, shuffle=True, class_weight=None, sample_weight=None, initial_epoch=0, steps_per_epoch=None, validation_steps=None)

x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size = 0.2, random_state = 42, stratify=labels)
print(y_train)
y_train = to_categorical(y_train, 12)

print('Features shape is: ' + str(x_train.shape))
print('Labels shape is: ' + str(y_train.shape))
print(y_train)


model.fit(
    x_train,
    y_train,
    epochs = 5,
    #steps_per_epoch = 2000,
    batch_size = 64)

#batch_size = 16
#model.fit_generator(
#        train_generator,
#        steps_per_epoch=2000,
#        epochs=50,
#        validation_data=validation_generator,
#        validation_steps=800)

testData = []
testImg = get_img('helmet.jpg')


resImg = get_resized_image(testImg, 128)
normImg = normalize_image(resImg)

testData.append(get_img_array(normImg))

testData = np.asarray(testData)
testData = testData.astype('float32')
testData /= 255

#print(testImg)

prediction = model.predict_classes(testData)
print('Prediction: ' + str(prediction))


#model.save_weights('first_try.h5')  # always save your weights after training or during training