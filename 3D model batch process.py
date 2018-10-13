‘’’
Process 3D models retrieved from 3D model API in batch.
Yuxuan Zhang
Wayfair
12/10/2018
‘’’

import os
import json
import urllib
import cStringIO
import scipy.misc
from pprint import pprint
import matplotlib.pyplot as plt

# get the JSON file from POSTMAN first
with open('response.json') as f:
    data = json.load(f)

# iterate through each model, show model class name, image, download zip and unzip it
for i in range(len(data)):
    print (data[i]['class_name'])
    
    # show image
    img_url = data[i]['thumbnail_image_url']
    img_url = img_url.replace('/43/','/47/')
    img_file = cStringIO.StringIO(urllib.urlopen(img_url).read())
    img = scipy.misc.imread(img_file)
    plt.imshow(img)
    plt.show()
    
    # download each zip file and unzip in a new folder
    sku = data[i]['sku']
    if not os.path.exists('temp/'+sku):
        os.makedirs('temp/'+sku)
    zip_url = data[i]['model']['obj']
    zip_response = requests.get(zip_url).content
    zipfile = ZipFile(StringIO(zip_response))
    zipfile.extractall('temp/'+sku)