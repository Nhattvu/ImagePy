#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# MY SOURCES
# https://www.codingforentrepreneurs.com/blog/extract-gps-exif-images-python/
# https://newbedev.com/how-to-iterate-over-files-in-a-given-directory
# https://stackoverflow.com/questions/64405326/django-exif-data-ifdrational-object-is-not-subscriptable

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from urllib.request import urlopen
import json
import os
import reverse_geocoder as rg
import time
import csv 
    

    
    
exif_data = None
image = None
directory = os.path.dirname(os.path.realpath(__file__))
processedCounter = 0
totalPicsCounter = 0


def get_exif_data(image):
    info = image._getexif()
    if info:
        for (tag, value) in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == 'GPSInfo':
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
    return exif_data


def get_if_exist(data, key):
    if key in data:
        return data[key]
    return None


def convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""

    degrees = value[0]
    minutes = value[1] / 60.0
    seconds = value[2] / 3600.0
    return degrees + minutes + seconds 


def get_lat_lng(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""

    lat = None
    lng = None

    if 'GPSInfo' in exif_data:
        gps_info = exif_data['GPSInfo']
        gps_latitude = get_if_exist(gps_info, 'GPSLatitude')
        gps_latitude_ref = get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = get_if_exist(gps_info, 'GPSLongitudeRef')
        if gps_latitude and gps_latitude_ref and gps_longitude \
            and gps_longitude_ref:
            lat = convert_to_degress(gps_latitude)
            if gps_latitude_ref != 'N':
                lat = 0 - lat
            lng = convert_to_degress(gps_longitude)
            if gps_longitude_ref != 'E':
                lng = 0 - lng
    return (lat, lng)

def get_camera_data(exif_data):
    """Returns the make and model of camera"""

    make = None
    model = None

    if 'GPSInfo' in exif_data:
        gps_info = exif_data['GPSInfo']
        gps_latitude = get_if_exist(gps_info, 'GPSLatitude')
        
       
    return (make, model)


def remove_undecoded_data(exif_data):
    exif_data.pop('MakerNote', None)
    exif_data.pop('PrintImageMatching', None)
    exif_data.pop('UserComment', None)
    exif_data.pop('XPTitle', None)
    return exif_data



for filename in os.listdir(directory):
        exif_data = None
        image = None
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.webp'): 
            totalPicsCounter = totalPicsCounter + 1
            img_path = os.path.join(directory, filename)
            print("\n\n\n",os.path.join(directory, filename,"\n"), flush=True)
            image = Image.open(img_path)
            exif_data = {}
            exif_data = get_exif_data(image)
            if(exif_data):
                processedCounter = processedCounter+1
                exif_data = remove_undecoded_data(exif_data)
                exif_data.get('Make')
                exif_data.get('Model')
                print(exif_data,"\n")
                #GET LAT LONG
                lat_long = get_lat_lng(exif_data)
                if(lat_long != (None, None)):
                    print(lat_long,"\n\n\n")
                    place = rg.search(lat_long) #place = getplace(*lat_long)
                    time.sleep(30)               
                    print(place)
        #rows.append([filename, ])
        else:
            continue
            
            

print("\n","Processed pictures: ", processedCounter)
print("\n","Total pictures: ",totalPicsCounter)
