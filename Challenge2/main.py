#! rm -rf /home/jupyter/notebooks/challenge1/data
#! rm -rf /home/jupyter/notebooks/challenge1/validation
#! rm -rf /home/jupyter/notebooks/challenge4

# ===

import os
import numpy as np

basePath = "/home/jupyter/notebooks"
imagesBasePath = "/home/jupyter/notebooks/images/gear_images"

dataPath = basePath + '/challenge1/data'
validationPath = basePath + '/challenge1/validation'
ch4Path = basePath + '/challenge4'

def get_subdirs(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def get_files(dir):
    return np.asarray(os.listdir(dir))

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(directory + ' created...')

create_directory_if_not_exists(dataPath)    
create_directory_if_not_exists(validationPath)
create_directory_if_not_exists(ch4Path)
        
for dir in get_subdirs(imagesBasePath):
    create_directory_if_not_exists(dataPath + '/' + dir)
    create_directory_if_not_exists(validationPath + '/' + dir)
    create_directory_if_not_exists(ch4Path + '/' + dir)

# ===

from sklearn.model_selection import train_test_split
from PIL import Image

def get_average_color(image):
    """ Returns a 3-tuple containing the RGB value of the average color of the
    given square bounded area of length = n whose origin (top left corner) 
    is (x, y) in the given image"""
    width, height = image.size
    r, g, b = 0, 0, 0
    count = 0
    for s in range(0, width):
        for t in range(0, height):
            pixlr, pixlg, pixlb = image.getpixel(s, t)
            r += pixlr
            g += pixlg
            b += pixlb
            count += 1
    return ((r/count), (g/count), (b/count))

def get_resized_image(image, desired_size):
    #im = Image.open(im_pth)
    old_size = image.size  # old_size[0] is in (width, height) format
    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])

    im = image.resize(new_size, Image.ANTIALIAS)

    #WHITE = (255, 255, 255)
    AVG_COLOR = get_average_color(im)
    
    new_im = Image.new("RGB", (desired_size, desired_size), AVG_COLOR)
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
    imgArr = np.array(new_im)
    normalizedArr = normalize(imgArr)
    return Image.fromarray(normalizedArr.astype('uint8'))
    

for dir in get_subdirs(imagesBasePath):
    path = os.path.join(imagesBasePath, dir)
    print('inside: ' + path)
    files = get_files(path)
    print('Found ' + str(len(files)) + ' in ' + dir)
    trainingSet, validationSet = train_test_split(files, train_size = 0.8, test_size = 0.2)
    
    print('Training files: ' + str(len(trainingSet)))
    print('Validation files: ' + str(len(validationSet)))
    
    for file in trainingSet:
        filePath = os.path.join(imagesBasePath, dir, file)
        im = Image.open(filePath, 'r')
        new_im = get_resized_image(im, 128)
        norm_im = normalize_image(new_im)
        targetPath = dataPath + '/' + dir + '/' + file
        print('Saving file to: ' + targetPath)
        norm_im.save(dataPath + '/' + dir + '/' + file)
        norm_im.save(ch4Path + '/' + dir + '/' + file)
        
    for file in validationSet:
        filePath = os.path.join(imagesBasePath, dir, file)
        im = Image.open(filePath, 'r')
        new_im = get_resized_image(im, 128)
        norm_im = normalize_image(new_im)
        targetPath = validationPath + '/' + dir + '/' + file
        print('Saving file to: ' + targetPath)
        norm_im.save(validationPath + '/' + dir + '/' + file)
        norm_im.save(ch4Path + '/' + dir + '/' + file)
        
# ===

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps
import cv2

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

desired_size = 128
im_pth = "/home/jupyter/notebooks/grumpycat.jpg"
    #'/home/jupyter/notebooks/images/gear_images/harnesses/10308642x1012549_zm.jpeg'

im = Image.open(im_pth)
originalArray = np.array(im)
plt.hist(originalArray.ravel(), 256, [0,256]); 
plt.show()


plt.imshow(im)
plt.show()
old_size = im.size  # old_size[0] is in (width, height) format

ratio = float(desired_size)/max(old_size)
new_size = tuple([int(x*ratio) for x in old_size])

im = im.resize(new_size, Image.ANTIALIAS)

WHITE = (255, 255, 255)
new_im = Image.new("RGB", (desired_size, desired_size), WHITE)
new_im.paste(im, ((desired_size-new_size[0])//2,
                    (desired_size-new_size[1])//2))

plt.imshow(new_im)
plt.show()
imgArr = np.array(new_im)
normalizedArr = normalize(imgArr)

normImg = Image.fromarray(normalizedArr.astype('uint8'))

plt.imshow(normImg)
plt.show()

#hist,bins = np.histogram(normImg.ravel(),256,[0,256])
x, y, _ = plt.hist(normalizedArr.ravel(), 256, [0,256]); 
plt.show()

print(x.max())
print(y.max())
# red
#rMin = imgArr[..., 0].min()
#rMax = imgArr[..., 0].max()
# green
#gMin = imgArr[..., 1].min()
#gMax = imgArr[..., 1].max()
# blue
#bMin = imgArr[..., 2].min()
#bMax = imgArr[..., 2].max()

#print('R: ' + str(rMin) + ' / ' + str(rMax))
#print('G: ' + str(gMin) + ' / ' + str(gMax))
#print('B: ' + str(bMin) + ' / ' + str(bMax))