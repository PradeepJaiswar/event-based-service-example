import os

from websocket import create_connection
from PIL import Image
import requests
import boto3
import time
import validators

from helpers import allowedFile, TMP_FILE_PATH, S3_BASE_URL, S3_BUCKET_NAME, WEB_SOCKET_PATH

def ResizeImage(url):
    if validators.url(url):
        # download the image from url and save for resizing
        fileName = url.split('/')[-1]
        if allowedFile(fileName):
            fileExtension = fileName.rpartition('.')[-1]
            S3fileExtension =  'jpeg' if fileExtension == 'jpg' else fileExtension
            downloadedFilePath = TMP_FILE_PATH + '/' + fileName;
            file = requests.get(url, allow_redirects=True)
            open(downloadedFilePath, 'wb').write(file.content)

            # Create thumbnail from downloaded image
            # Leept the aspect ratio
            # Max image size in 640, 480
            # Read the image, resize and save as a temporary file
            SIZE = (640, 480)
            image = Image.open(downloadedFilePath)
            image.thumbnail(SIZE, Image.ANTIALIAS)
            resizedFilePath = TMP_FILE_PATH + '/' + str(int(time.time())) + '-resized-' + fileName
            image.save(resizedFilePath, S3fileExtension )

            # save image in AWS S3 Bucket 
            data = open(resizedFilePath, 'rb')
            s3 = boto3.resource('s3')
            
            s3FilePath = 'resized/'+ str(int(time.time())) + '-resized-' + fileName ;
            s3FileUrl = S3_BASE_URL + '/' + s3FilePath;
            s3.Bucket(S3_BUCKET_NAME).put_object(
                ACL='public-read',
                Key=s3FilePath,
                Body=data,
                ContentType='image/' + S3fileExtension
            )

            # publish to socket that image image in resized and uploaded to AWS S3 Bucket 
            ws = create_connection(WEB_SOCKET_PATH)
            ws.send(s3FileUrl)
            ws.close()

            return s3FileUrl  

    return False 
        

