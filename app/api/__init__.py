from flask import Blueprint
from flask_restful import Api

apiBlueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(apiBlueprint)

# Import the resources
from . import upload  # NOQA
from . import images  # NOQA
