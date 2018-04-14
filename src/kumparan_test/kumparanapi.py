#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following line in the
entry_points section in setup.py:

    [console_scripts]
    fibonacci = kumparan_test.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""
from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging
from pymongo import MongoClient,ASCENDING
from bson.objectid import ObjectId
from flask import Flask, json, request,jsonify

from kumparan_test.model import Model


from src.kumparan_test import __version__

__author__ = "teguhcf"
__copyright__ = "teguhcf"
__license__ = "mit"

_logger = logging.getLogger(__name__)

# from flask import Flask, jsonify, abort, make_response, request, Response
# from flask.ext.pymongo import PyMongo
# from bson.json_util import dumps
# from bson.objectid import ObjectId


application = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.kumparan

model = Model()


@application.route("/api/v1/news/add", methods=['POST'])
def addNews():
    try:
        json_data = request.json['data']
        model.addNews(json_data)
        return jsonify(status='OK', message=' News inserted successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@application.route("/api/v1/news/getlist", methods=['GET'])
def getNewsList():
    try:
        status = request.args.get('status')
        topic_id = request.args.get('topic_id')
        data = model.getNewsList(status,topic_id)

    except Exception as e:
        return str(e)
    return json.dumps(data)
    # return mongo_to_jsonResponse(machines)


@application.route('/api/v1/news/get', methods=['GET'])
def getNews():
    try:
        id = request.args.get('id')
        data = model.getNews(id)
        return json.dumps(data)
        # return mongo_to_jsonResponse(machine)
    except Exception as e:
        return str(e)


@application.route("/api/v1/news/delete", methods=['DELETE'])
def deleteNews():
    try:
        id = request.args.get('id')
        # machineId = request.json['id']
        res = db.news.find_one({'_id': ObjectId(id)})
        if res is None: return jsonify(status='ERROR', message="Data not exist")

        db.news.remove({'_id': ObjectId(id)})
        return jsonify(status='OK', message='deletion successful')
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))



@application.route('/api/v1/news/update', methods=['POST'])
def updateNews():
    try:

        json_data = request.json['data']
        res = model.updateNews(json_data)
        if res is False: return jsonify(status='ERROR', message="Data not exist")
        return jsonify(status='OK', message='updated successfully')
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@application.route("/api/v1/topic/add", methods=['POST'])
def addTopic():
    try:
        json_data = request.json['data']
        model.addTopic(json_data)
        print("hhhhhhhhh")
        return jsonify(status='OK', message='Topic inserted successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@application.route('/api/v1/topic/update', methods=['PUT'])
def updateTopic():
    try:

        json_data = request.json['data']
        res = model.updateTopic(json_data)
        if res is False: return jsonify(status='ERROR', message="Data not exist")

        return jsonify(status='OK', message='updated successfully')
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))



@application.route("/api/v1/topic/getlist", methods=['GET'])
def getTopicList():
    try:
        topics = db.topic.find().sort([("topic_id", ASCENDING)])
    except Exception as e:
        return str(e)
    # return json.dumps(machines)
    return model.mongo_to_jsonResponse(topics)


@application.route("/api/v1/topic/get", methods=['GET'])
def getTopic():
    try:
        id = request.args.get('id')
        data = db.topic.find_one({'topic_id': int(id)})
    except Exception as e:
        return str(e)
    # return json.dumps(machines)
    return model.mongo_to_jsonResponse(data)


@application.route("/api/v1/topic/delete", methods=['DELETE'])
def deleteTopic():
    try:
        id = request.args.get('id')
        # machineId = request.json['id']
        res = db.topic.find_one({'topic_id': int(id)})
        if res is None: return jsonify(status='ERROR', message="Data not exist")

        db.topic.remove({'topic_id': int(id)})
        return jsonify(status='OK', message='deletion successful')
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))




if __name__ == "__main__":
    application.run(host='0.0.0.0')

