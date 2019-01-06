import os
from dotenv import load_dotenv

# get the env varible
load_dotenv()
TMP_FILE_PATH = os.getenv('TMP_FILE_PATH');
S3_BASE_URL = os.getenv('S3_BASE_URL');
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME');
WEB_SOCKET_PATH = os.getenv('WEB_SOCKET_PATH');


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS