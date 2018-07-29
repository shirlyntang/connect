from google.cloud import vision
from google.cloud.vision import types

client = vision.ImageAnnotatorClient()
image = vision.types.Image()
pic = 'bobaguys'
image.source.image_uri = 'gs://shipper-pics/' + pic + '.png'
resp = client.text_detection(image=image)
print('\n'.join([d.description.lower() for d in resp.text_annotations]))
