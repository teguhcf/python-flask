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
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, render_template, jsonify, json, request,jsonify,Response,abort,make_response

from bson.json_util import dumps

from kumparan_test.model import Model

import datetime


from mongojoin.mongojoin import MongoJoin
from mongojoin.mongocollection import MongoCollection

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


def mongo_to_jsonResponse(mongobj):
    # dumps function convert mongo object into json
    js = dumps(mongobj)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@application.route("/api/v1/news/add", methods=['POST'])
def addNews():
    try:
        json_data = request.json['data']
        title = json_data['title']
        content = json_data['content']
        topic_id = json_data['topic_id']
        status=json_data['status']
        user_id=json_data['user_id']
        created_at=datetime.datetime.utcnow()

        # topic_detail = db.topic.find({"topic_id": {"$in": topic_id}})
        #
        #
        # topicList = []
        # for machine in topic_detail:
        #     machineItem = {
        #         'topic_id': machine['topic_id'],
        #         'topic': machine['topic'],
        #         # 'news': machine['news']
        #         'topic_desc' : machine['topic_desc']
        #     }
        #     topicList.append(machineItem)

        db.news.insert_one({
            'title': title, 'content': content, 'topic_id':topic_id, 'status' : status,
            'user_id':user_id, 'created_at':created_at
        })
        return jsonify(status='OK', message=' News inserted successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@application.route("/api/v1/news/getlist", methods=['GET'])
def getNewsList():
    try:
        data = model.getNewsList()
        print("masssss")
    except Exception as e:
        return str(e)
    return json.dumps(data)
    # return mongo_to_jsonResponse(machines)


@application.route("/api/v1/topic/add", methods=['POST'])
def addTopic():
    try:
        json_data = request.json['data']
        topic_id = json_data['topic_id']
        topic = json_data['topic']
        # news_id = json_data['news']
        topic_desc = json_data['topic_desc']

        # news = db.topic.find({"topic_id": {"$in": news_id}})
        #
        db.topic.insert_one({
            'topic_id': topic_id, 'topic': topic, 'topic_desc':topic_desc
        })
        return jsonify(status='OK', message='Topic inserted successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))

@application.route('/')
def showMachineList():
    return render_template('list.html')


@application.route('/api/v1/news/get', methods=['GET'])
def getNews():
    try:

        # all_menus = mongo.db.menus.find()


        id_machine = request.args.get('id')
        print("ini id machine", id_machine)
        # machineId = request.json['id']
        machineId=request.args.get('id')
        machine = db.news.find_one({'_id': ObjectId(machineId)})
        # machineDetail = {
        #     'id': str(machine['_id']),
        #     'judul': machine['judul'],
        #     'content': machine['content'],
        #     'topic':machine['topic']
        # }
        # return json.dumps(machineDetail)
        return mongo_to_jsonResponse(machine)
    except Exception as e:
        return str(e)


@application.route('/api/v1', methods=['POST'])
def updateMachine():
    try:
        machineInfo = request.json['data']
        machineId = machineInfo['id']
        device = machineInfo['device']
        ip = machineInfo['ip']
        username = machineInfo['username']
        db.news.update_one({'_id': ObjectId(machineId)},
                                 {'$set': {'date': device, 'tweet': ip, 'lable': username}})
        return jsonify(status='OK', message='updated successfully')
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@application.route('/api/v1/news/update', methods=['POST'])
def updateNews():
    try:
        # machineInfo = request.json['data']
        # machineId = machineInfo['id']
        # device = machineInfo['device']
        # ip = machineInfo['ip']
        # username = machineInfo['username']

        json_data = request.json['data']
        news_id = json_data['news_id']
        title = json_data['title']
        content = json_data['content']
        topic_id = json_data['topic_id']
        status=json_data['status']
        user_id=json_data['user_id']
        last_modified=datetime.datetime.utcnow()

        res = db.news.find_one({'_id': ObjectId(news_id)})
        if res is None: return jsonify(status='ERROR', message="Data not exist")


        db.news.update_one({'_id': ObjectId(news_id)},
                                 {'$set': {'title': title, 'content': content, 'topic_id': topic_id, 'status':status,
                                           'user_id':user_id, 'last_modified':last_modified
                        }})
        return jsonify(status='OK', message='updated successfully')
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))



@application.route('/api/v1/topic/update', methods=['POST'])
def updateTopic():
    try:

        json_data = request.json['data']
        topic_id = json_data['topic_id']
        topic = json_data['topic']
        # news_id = json_data['news']
        topic_desc = json_data['topic_desc']

        # last_modified=datetime.datetime.utcnow()

        res = db.topic.find_one({'topic_id': topic_id})
        if res is None: return jsonify(status='ERROR', message="Data not exist")


        db.topic.update_one({'topic_id': topic_id},
                                 {'$set': {'topic': topic, 'topic_desc': topic_desc
                        }})

        return jsonify(status='OK', message='updated successfully')
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))








@application.route("/api/v1/topic/getlist", methods=['GET'])
def getTopicList():
    try:
        # print("masuk get machine lst")
        # id_machine = request.args.get('id')
        # print("ini id machine", id_machine)
        # coll.find({"SPCOMNAME": {"$in": ['paddlefish', 'lake sturgeon']}})

        # machines = db.topic.find({"topic_id":{"$in": [1,2]}})
        machines = db.topic.find()
        # machineList = []
        # for machine in machines:
        #
        #     machineItem = {
        #         'id': str(machine['_id']),
        #         'topic_id': str(machine['topic_id']),
        #         'topic': machine['topic'],
        #         'news': machine['news']
        #     }
        #     machineList.append(machineItem)

    except Exception as e:
        return str(e)
    # return json.dumps(machines)
    return mongo_to_jsonResponse(machines)

@application.route("/execute", methods=['POST'])
def execute():
    try:
        machineInfo = request.json['data']
        ip = machineInfo['ip']
        username = machineInfo['username']
        password = machineInfo['password']
        command = machineInfo['command']
        isRoot = machineInfo['isRoot']

        env.host_string = username + '@' + ip
        env.password = password
        resp = ''
        with settings(warn_only=True):
            if isRoot:
                resp = sudo(command)
            else:
                resp = run(command)

        return jsonify(status='OK', message=resp)
    except Exception as e:
        print('Error is ' + str(e))
        return jsonify(status='ERROR', message=str(e))


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


@application.route("/api/v1/topic/delete", methods=['DELETE'])
def deleteTopic():
    try:
        id = request.args.get('id')
        # machineId = request.json['id']
        res = db.topic.find_one({'_id': ObjectId(id)})
        if res is None: return jsonify(status='ERROR', message="Data not exist")

        db.topic.remove({'_id': ObjectId(id)})
        return jsonify(status='OK', message='deletion successful')
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@application.route("/deleteMachine", methods=['POST'])
def deleteM():
    try:
        machineId = request.json['id']
        db.news.remove({'_id': ObjectId(machineId)})
        return jsonify(status='OK', message='deletion successful')
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


if __name__ == "__main__":
    application.run(host='0.0.0.0')

