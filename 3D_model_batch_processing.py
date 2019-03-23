'''
Process 3D models retrieved from 3D model API in batch.
Yuxuan (Tim) Zhang
Wayfair
Oct 18, 2018
'''

import sys
import os
import json
import requests
import urllib
from io import StringIO
#import cStringIO
import scipy.misc
#from StringIO import StringIO
from zipfile import ZipFile
from urllib.request import urlopen
#import matplotlib.pyplot as plt

def get_models(username, api_key):
    """ Send a GET request to Wayfair 3D model API to get all 3D models
        
        Args:
        username: API username
        api_key: API key
        
        Returns:
        A JSON response for 3D model information
    """
    
    url = "https://wayfair.com/3dapi/models"

    # use session to send auth and header along with every request
    session = requests.Session()
    session.auth = (username, api_key)
    session.headers = {'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36'}
    session.get(url)
    response = session.get(url)
    return response.json()

def unzip_and_save_models(data, num_to_process):
    """ Given the returned JSON, download the zip files
        for OBJ models and save them to local folder
        
        Args:
        data: the returned JSON
        num_to_process: number of 3D models to process
    """
    save_dir = 'Wayfair 3D Models/'
    
    try:
        if num_to_process == 'all':
            num_to_process = 200
        else:
            num_to_process = int(num_to_process)
    except:
        num_to_process = 200
    
    for i in range(len(data))[:num_to_process]:
        print (i, data[i]['class_name'])
        sku = data[i]['sku']
        
        # show image
        img_url = data[i]['thumbnail_image_url']
        img_url = img_url.replace('/43/','/47/')
        #img_file = StringIO(urlopen(img_url).read())
        
        resource = urllib.request.urlopen(img_url)
        content =  resource.read().decode(resource.headers.get_content_charset())
        
        img_file = StringIO(content)
        
        img = scipy.misc.imread(img_file)
        #plt.imshow(img)
        #plt.show()
        
        # download each zip file and unzip in a new folder
        if not os.path.exists(save_dir+sku):
            os.makedirs(save_dir+sku)
        zip_url = data[i]['model']['obj']
        zip_response = requests.get(zip_url).content
        zipfile = ZipFile(StringIO(zip_response))
        zipfile.extractall(save_dir+sku)
        # save example image
        scipy.misc.imsave(save_dir+sku+'/'+sku+'.png', img)

if __name__ == '__main__':
    '''Run the script by specifying parameters needed
        
        Args:
        argv[0]: script name: 3D_model_batch_process.py
        argv[1]: API username E.G. abc@gmail.com
        argv[2]: API key. E.G. 12345abcde
        argv[3]: Number of 3D models to process. E.G. 5 or all
        
        Returns:
        Calls the API to get all 3D models back
        After unzip each OBJ zip file, save it to a local folder: Wayfair 3D Models/
        
        E.G. In command line, run: python 3D_model_batch_processing.py abc@gmail.com 12345abcde 5
    '''
    if len(sys.argv)==4:
        
            
        username = str(sys.argv[1])
        api_key = str(sys.argv[2])
        num_to_process = sys.argv[3]

        # Send a GET request to Wayfair 3D model API to get the JSON for all 3D models
        response = get_models(username, api_key)
        print ('Number of returned 3D models: ',len(response))
    
        if len(response) != 188:
            print ('''
                If you are only getting 5 models back, this is probably because
                you are entering wrong username/api_key. Make sure you signed
                up for an API key at https://wayfair.com/3dapi
                ''')
        
        print ('\n')
        print ('Now downloading 3D models to Wayfair 3D Models/ folder')
    
        # Given the returned JSON, download the zip files
        # for OBJ models and save them to local folder
        unzip_and_save_models(response, num_to_process)

    else:
        print ('please provide all arguments.')
        print ('''
            Args:
            argv[0]: script name: 3D_model_batch_process.py
            argv[1]: API username E.G. abc@gmail.com
            argv[2]: API key. E.G. 12345abcde
            argv[3]: Number of 3D models to process. E.G. 5 or all
            
            E.G. python 3D_model_batch_processing.py abc@gmail.com 12345abcde 5
            E.G. python 3D_model_batch_processing.py abc@gmail.com 12345abcde all
            ''')
