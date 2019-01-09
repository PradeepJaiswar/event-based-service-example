from flask_restful import Resource
from app.api import api
import boto3

from helpers import S3_BASE_URL, S3_BUCKET_NAME

class ImageResource(Resource):  
    def get(self):
        s3ImagesList = []      
        s3 = boto3.resource('s3')
        s3Bucket = s3.Bucket(S3_BUCKET_NAME)
        # get files which are in resized folder
        for objectSummary in s3Bucket.objects.filter(Prefix="resized/"):
            if objectSummary.key[-1] != "/":
                s3ImagesList.append(S3_BASE_URL + '/' + objectSummary.key)
        return {
            'data': s3ImagesList,
        },200
        
api.add_resource(ImageResource, '/images')
