# Cvent based service example

### Event based services for uploading images to AWS S3 bucket. Resizing uploaded images to thumbnail, uploading them into separate S3 bucket folder and listing down the resized images.

## Demo
For demo visit http://13.126.151.86/

## How it works?

Upload service uploads the original image to AWS S3 bucket and returns the message saying that image is uploaded and sent for resizing. At the same time upload service adds a job in Redis queue that new image is ready for resizing. Image resize worker which is listening for the new job from Redis, picks up the job and does the resizing of original image and uploads back to AWS S3 in a separate folder. After the worker is done with resizing and uploading it also sends a message to a web socket server that new image is being resized in the system. On receiving the message from web worker web socket server tell all subscribed client that new resized image is added in the system, update your UI

## Architecture Diagram
![architecture-diagram](https://raw.githubusercontent.com/PradeepJaiswar/event-based-service-example/master/architecture-diagram.png)

## Service components

### REST API

#### Pre-requisites
installed python and pip

#### Install dependencies

```
$ pip install virtualenv  #make sure you do this
$ virtualenv .pyenv
$ source .pyenv/bin/activate
$ pip install -r requirements.txt
```

#### Run

```
$ python run.py
* Running on http://localhost:7000/ (Press CTRL+C to quit)
```
#### API's

PORT :: 7000

Upload API 

`http://localhost:7000/api/upload` - POST

params:
```
 name : file
 Form Data: file(binary)
```
Header:
```
Content-Type: multipart/form-data
```
List resized images API

`http://localhost:7000/api/images` - GET 

#### AWS SE bucket access credentials

Install and configure aws cli

https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html

https://docs.aws.amazon.com/cli/latest/reference/configure/

#### Enviroment variable

Create a .env file on each enviroment in root of repo
```
TMP_FILE_PATH = ''; # tmp file storage path on server
S3_BUCKET_NAME = ''; # S3 bucket name
S3_BASE_URL = ''; # S3 bucket base url 
WEB_SOCKET_PATH = ''; # websocket server path
```


### Redis Server 

#### Install dependencies

install redis https://redis.io/topics/quickstart

#### Run redis server
```
redis-server
```

### Queue and Worker
RQ (Redis Queue) :: A simple Python library for queueing jobs and processing them in the background with workers. 

#### Install dependencies

Already include in the project requirements.txt file

Worker file is at https://github.com/PradeepJaiswar/event-based-service-example/blob/master/worker.py

#### Run rq worker

```
cd event-based-service-example
rq worker
```
### WebSocket
PORT :: 8080

e.g ws://localhost:8080/

#### Prerequisites
installed node and npm

#### Install dependencies
```
cd event-based-service-example
npm install ws
```
Websocket server file is at https://github.com/PradeepJaiswar/event-based-service-example/blob/master/socket-server.js

#### Run websocket server

```
cd event-based-service-example
node socket-server.js or nodejs socket-server.js
```

## Web applicatios

Check https://github.com/PradeepJaiswar/open-table-exercise-frontend

## Test 

TODO

## Code 

APi's are written Flaskframewoek http://flask.pocoo.org/ using blueprints http://flask.pocoo.org/docs/1.0/blueprints/ for modular code structure






