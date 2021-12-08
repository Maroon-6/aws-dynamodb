import os

from flask import Flask, Response, request, redirect, url_for
from flask_cors import CORS
import json
import logging
import re
from datetime import datetime
from dynamo import dynamodb as db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)

##################################################################################################################

@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'


@app.route("/comments", methods=["GET", "POST"])
def comments():
    if request.method == "GET":
        qs = request.query_string
        if not qs:
            res = db.do_a_scan("comments")
        else:
            tmp = {}
            for item in str(qs, "utf-8").split("&"):
                k, v = item.split("=")
                tmp[k] = re.sub(r"%20", " ", v)
            res = db.find_by_template("comments", tmp)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == "POST":
        data = request.json
        email = data["email"]
        comment = data["comment"]
        recipe = data["recipe"]
        res = db.add_comment(email, comment, recipe)
        rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
        return rsp


@app.route("/comments/<comment_id>", methods=["GET", "POST", "PUT"])
def comment_by_id(comment_id):
    if request.method == "GET":
        res = db.get_item("comments",
                          {
                              "comment_id": comment_id
                          })
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    elif request.method == "POST":
        data = request.json
        commenter = data["email"]
        response = data["response"]
        res = db.add_response("comments", comment_id, commenter,
                              response)
        rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
        return rsp
    elif request.method == "PUT":
        data = request.json
        comment = db.get_item("comments", {"comment_id": comment_id})
        old_version_id = comment["version_id"]
        comment["comment"] = data["comment"]
        try:
            res = db.write_comment_if_not_changed(comment, old_version_id)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        except Exception as e:
            rsp = Response(json.dumps(e, default=str), status=200, content_type="application/json")
        return rsp



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050)
