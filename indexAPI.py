from crypt import methods
from os import abort, getcwd, path
import os
import cv2
import numpy as np
from flask import Flask, json, request, Response
import utils

app = Flask(__name__)

@app.route("/picture/",methods=["GET"])
def post_add():
    if not request.data:
        abort(400)
    with open("encodedData.json","w+") as f:
        f.write(request.data.decode("utf-8"))
    return request.data.decode("utf-8")

@app.route("/picture/filterImg/",methods=["GET"])
def get_filter():
    path = request.headers.get('path')
    blur = utils.filterImg(path)
    blur = getcwd() + os.sep + blur
    return blur

@app.route("/picture/canny/", methods=["GET"])
def get_canny():
    path = request.headers.get('path')
    outCanny = utils.CannyDetection(path)
    outCanny = getcwd() + os.sep + outCanny
    return outCanny

@app.route("/picture/face/", methods=["GET"])
def get_face():
    path = request.headers.get('path')
    face = utils.FaceRec(path)
    face = getcwd() + os.sep + face
    return face

@app.route("/myip", methods=["GET"])
def get_my_ip():
    return request.remote_addr, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)