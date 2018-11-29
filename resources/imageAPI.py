from flask import request
from flask_restful import Resource
from flask_uploads import UploadSet, UploadNotAllowed
from models.image import Image, db
from datetime import datetime

acao = {"Access-Control-Allow-Origin": "*"}

images = UploadSet("IMAGE")


class ImageAPI(Resource):
    @staticmethod
    def post():
        try:
            filename = images.save(request.files['image'])
        except KeyError:
            return {"error": "Image not found"}, 404, acao
        except UploadNotAllowed:
            return {"error": "File type not supported"}, 403, acao
        name = request.form["name"]
        image = Image(name=name, physical_name=filename, url=images.url(filename), upload_time=datetime.now())
        db.session.add(image)
        db.session.commit()
        return {"name": image.name, "url": image.url}, 201, acao

    @staticmethod
    def get():
        name = request.args.get("name")
        image = Image.query.filter_by(name=name).first()
        if image is None:
            return {"error": "Image not found"}, 404, acao
        return {"url": image.url}, 200, acao
