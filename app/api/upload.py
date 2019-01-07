import os
import time
import time
import boto3
from flask_restful import Resource
from flask import request
from werkzeug.utils import secure_filename
from redis import Redis
from rq import Queue

from app.api import api
from worker import ResizeImage

from helpers import allowedFile, S3_BASE_URL, S3_BUCKET_NAME, TMP_FILE_PATH

class UploadResource(Resource):  
    def post(self):
        file = request.files['file']
        if file and allowedFile(file.filename):
            try:
                fileName = secure_filename(file.filename).lower()
                fileExtension = fileName.rpartition('.')[-1].lower()
                file.save(os.path.join(TMP_FILE_PATH, fileName))
                
                # send the file to AWS S3 bucket  
                S3fileExtension =  'jpeg' if fileExtension == 'jpg' else fileExtension
                s3FilePath = 'original/'+ str(int(time.time())) + '-original-' + fileName ;
                s3FileUrl = S3_BASE_URL + '/' + s3FilePath;
                data = open(os.path.join(TMP_FILE_PATH, fileName), 'rb')
                s3 = boto3.resource('s3')
                s3.Bucket(S3_BUCKET_NAME).put_object(
                    ACL='public-read',
                    Key=s3FilePath,
                    Body=data,
                    ContentType='image/' + S3fileExtension
                )
                
                # send to redis queue to pick by resize worker
                redisQueue = Queue(connection=Redis())
                redisQueue.enqueue(ResizeImage, s3FileUrl)  
            except Exception as e:
                print(e);
                return {
                    'data': 'something went wrong',
                },400 

            return {
                'data': s3FileUrl,
            },200
        else:
            return {
                'data': 'bad request',
            },400   

api.add_resource(UploadResource, '/upload')
