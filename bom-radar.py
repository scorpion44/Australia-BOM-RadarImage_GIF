#!/usr/bin/env python3
import io
import ftplib
from PIL import Image

import sys

new_args=sys.argv
#print (sys.argv)
new_args.pop(0)
tag=new_args.pop(0)

product_id = tag    #'IDR664' # The ID for our radar image
frames = [] # List to store the images
# The layers that we want
layers = ['background', 'catchments', 'topography', 'locations']
ftp = ftplib.FTP('ftp.bom.gov.au')
ftp.login()
ftp.cwd('anon/gen/radar_transparencies/')
for layer in layers:
 filename = f'{product_id}.{layer}.png'
 file_obj = io.BytesIO()
 ftp.retrbinary('RETR ' + filename, file_obj.write)
 if layer == 'background':
  base_image = Image.open(file_obj).convert('RGBA')
 else:
  image = Image.open(file_obj).convert('RGBA')
  base_image.paste(image, (0,0), image)
# Access the FTP server
ftp = ftplib.FTP('ftp.bom.gov.au')
ftp.login()
ftp.cwd('anon/gen/radar/')
# List comprehension to filter out the images we need
# Make sure the filename starts with the radar ID, and it ends with .png
# Take the last 5 images, since it is the most recent ones
files = [file for file in ftp.nlst() \
 if file.startswith(product_id) \
 and file.endswith('.png')][-5:]
# Loop over the files and append the image data into our image list
for file in files:
 file_obj = io.BytesIO()
 try:
  ftp.retrbinary('RETR ' + file, file_obj.write)
  image = Image.open(file_obj).convert('RGBA')
  frame = base_image.copy()
  frame.paste(image, (0,0),image)
  frames.append(frame)
 except ftplib.all_errors:
  pass
ftp.quit()
# Store the result as a GIF file
frames[0].save(tag + '.gif', format='GIF',
 save_all=True,
 append_images=frames[1:]+[frames[-1],frames[-1]],
 duration=400,
 loop=0)
