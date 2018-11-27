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
        name = request.form["name"]
        if Image.query.filter_by(name=name).first() is not None:
            return {"error": "Image name has already been taken."}, 403, acao
        try:
            filename = images.save(request.files['image'])
        except KeyError:
            return {"error": "Image not found"}, 404, acao
        except UploadNotAllowed:
            return {"error": "File type not supported"}, 406, acao
        image = Image(name=name, physical_name=filename, url=images.url(filename), upload_time=datetime.now())
        db.session.add(image)
        db.session.commit()
        return {"filename": filename, "url": image.url}, 201, acao

    @staticmethod
    def get():
        name = request.args.get("name")
        image = Image.query.filter_by(name=name).first()
        if image is None:
            return {"error": "Image not found"}, 404, acao
        return {"url": image.url}, 200, acao
