import os
from urllib.request import urlopen, urlretrieve

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(directory + ' created...')
        
def download_and_save_file(url, path):
    url = str(url).replace('b\'http', 'http').replace('\\r\\n\'', '')
    tokens = url.split('/')
    fileName = tokens[-1]
    urlretrieve(url, path + '/' + fileName)
    print('Azure --(' + fileName + ')--> ' + path)
    
def get_file_name(url):
    tokens = url.split('/')
    return tokens[-1]

basePath = './'
modelPath = basePath + 'model'

models = {  'alexnet': 'https://www.cntk.ai/Models/CNTK_Pretrained/AlexNet_ImageNet_CNTK.model',
            'resnet': 'https://www.cntk.ai/Models/CNTK_Pretrained/ResNet18_ImageNet_CNTK.model'}

selectedModel = 'resnet'

modelFileName = get_file_name(models[selectedModel])
create_directory_if_not_exists(modelPath)
download_and_save_file(models[selectedModel], modelPath)
