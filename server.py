from flask import Flask, send_file, request
from flask_restful import Resource, Api
import requests
import os
import numpy as np
from PIL import Image
from mozaika import Mozaika

app = Flask(__name__)
api = Api(app)

class MozaikaEndpoint(Resource):
    def get(self):
        mozaika = Mozaika(request.args)

        if mozaika.valid:
            file_name = 'image.jpeg'
            
            image = mozaika.generateImage()
            image.save(file_name)

            return send_file(file_name, mimetype='image/jpeg')

        else:
            return 'Niepoprawne argumenty: ' + str(mozaika.invalidArguments), 400

api.add_resource(MozaikaEndpoint, '/mozaika')

if __name__ == '__main__':
    app.run(debug=True)