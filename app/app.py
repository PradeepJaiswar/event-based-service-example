import os
from flask import Flask

from config.base import BaseConfig
from api import apiBlueprint

from flask_cors import CORS

# For import *
__all__ = ['createApp']

def createApp(config=None, appName=None, blueprints=None):
   """Create a Flask app."""

   if appName is None:
     appName = BaseConfig.PROJECT

   app = Flask(appName, instance_path=os.path.join('/tmp', 'instance'), instance_relative_config=True)
   configureApp(app, config)
   registerBlueprints(app)
   enableCors(app)
   return app

def configureApp(app, config=None):   
   app.config.from_object(BaseConfig)

   if config:
     app.config.from_object(config)
     return

def registerBlueprints(app):
    app.register_blueprint(apiBlueprint)

def enableCors(app):
    CORS(app)
    pass