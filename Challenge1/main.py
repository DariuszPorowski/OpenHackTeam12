# ! unzip /home/jupyter/notebooks/gear_images.zip -d /home/jupyter/notebooks/images

from azure.cognitiveservices.vision.customvision.prediction import prediction_endpoint
from azure.cognitiveservices.vision.customvision.prediction.prediction_endpoint import models

# Now there is a trained endpoint that can be used to make a prediction
prediction_key = "2772bb35446348b1aa413a902f0dfa54"
projectId = "2eb6c4ae-9771-495b-aa3b-42f0c5712b4e" #"eb6c4ae-9771-495b-aa3b-42f0c5712b4e"
iterationId = "e96a0708-fbb4-4bbb-a744-7311ece71ca7"
predictor = prediction_endpoint.PredictionEndpoint(prediction_key)

# test_img_url = base_image_url + "Images/Test/test_image.jpg"
#results = predictor.predict_image_url(project.id, iteration.id, url=test_img_url)

# Alternatively, if the images were on disk in a folder called Images alongside the sample.py, then
# they can be added by using the following.
#
# Open the sample image and get back the prediction results.
with open("/home/jupyter/notebooks/images/gear_images/hardshell_jackets/10300522x1076923_zm.jpeg", mode="rb") as test_data:
    results = predictor.predict_image(projectId, test_data, iterationId)

# Display the results.
for prediction in results.predictions:
    print ("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))