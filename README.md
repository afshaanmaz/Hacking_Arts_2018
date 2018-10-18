# Hacking Arts 2018
# Script for Getting 3D Models from Wayfair 3D Model API and Batch Process them

## Major Required Libraries
urllib

zipfile

requests

cStringIO

## Usage
First sign up for Wayfair 3D model API at [bit.ly/wayfair3dapi](bit.ly/wayfair3dapi)

Run the following in command line

Args:
- argv[0]: script name: 3D_model_batch_process.py
- argv[1]: API username E.G. abc@gmail.com
- argv[2]: API key. E.G. 12345abcde
- argv[3]: Number of 3D models to process. E.G. 5 or all
```
python 3D_model_batch_processing.py your_username api_key all
```
