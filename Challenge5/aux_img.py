from PIL import Image
import numpy as np

# Converts the PIL Image to numpy array
def get_img_array(img):
    return np.array(img)

def get_resized_image(image, desired_size):
    old_size = image.size
    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])

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