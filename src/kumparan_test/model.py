
from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging
from pymongo import MongoClient,DESCENDING
from bson.objectid import ObjectId
from flask import Response

from bson.json_util import dumps
import datetime

client = MongoClient('localhost', 27017)
db = client.kumparan

class Model:

    def mongo_to_jsonResponse(self,mongobj):
        # dumps function convert mongo object into json
        js = dumps(mongobj)
        resp = Response(js, status=200, mimetype='application/json')
        return resp


    def addNews(self,json_data):
        title = json_data['title']
        content = json_data['content']
        topic_id = json_data['topic_id']
        status = json_data['status']
        user_id = json_data['user_id']
        created_at = datetime.datetime.utcnow()
        last_modified=datetime.datetime.utcnow()

        db.news.insert_one({
            'title': title, 'content': content, 'topic_id': topic_id, 'status': status,
            'user_id': user_id, 'created_at': created_at, 'last_modified':last_modified
        })


    def getNewsList(self,status,topic_id):
        if (status is not None):
            data = db.news.find({"status": status}).sort([("created_at", DESCENDING)])
            print("status", status)
        elif topic_id is not None:
            print("topic", topic_id)
            # arr_status=[status]
            data = db.news.find({"topic_id": {"$in": [int(topic_id)]}}).sort([("created_at", DESCENDING)])

        else:
            print("else")
            data = db.news.find().sort([("created_at", DESCENDING)])

        news_list = []
        for news in data:
            topic_detail = db.topic.find({"topic_id": {"$in": news['topic_id']}})
            topicList = []
            for topic in topic_detail:
                topicItem = {
                    'topic_id': topic['topic_id'],
                    'topic': topic['topic'],
                    # 'news': machine['news']
                    'topic_desc': topic['topic_desc']
                }
                topicList.append(topicItem)

            newsItem = {
                'id': str(news['_id']),
                'title': news['title'],
                'content': news['content'],
                'topic_id': news['topic_id'],
                'topic_detail': topicList,
                'status': news['status'],
                'user_id': news['user_id'],
                'created_at': news['created_at'],
                'last_modified': news['last_modified']
            }
            news_list.append(newsItem)

        return news_list


    def getNews(self,news_id):
        news_data = db.news.find_one({'_id': ObjectId(news_id)})
        topic_detail = db.topic.find({"topic_id": {"$in": news_data['topic_id']}})
        topicList = []
        for topic in topic_detail:
            topicItem = {
                'topic_id': topic['topic_id'],
                'topic': topic['topic'],
                # 'news': topic['news']
                'topic_desc': topic['topic_desc']
            }
            topicList.append(topicItem)
        news = {
            'id': str(news_data['_id']),
            'title': news_data['title'],
            'content': news_data['content'],
            'topic_id': news_data['topic_id'],
            'topic_detail': topicList,
            'status': news_data['status'],
            'user_id': news_data['user_id'],
            'created_at': news_data['created_at']
        }
        return news


    def updateNews(self,json_data):
        news_id = json_data['news_id']
        title = json_data['title']
        content = json_data['content']
        topic_id = json_data['topic_id']
        status = json_data['status']
        user_id = json_data['user_id']
        last_modified = datetime.datetime.utcnow()

        res = db.news.find_one({'_id': ObjectId(news_id)})
        if res is None: return False

        db.news.update_one({'_id': ObjectId(news_id)},
                           {'$set': {'title': title, 'content': content, 'topic_id': topic_id, 'status': status,
                                     'user_id': user_id, 'last_modified': last_modified
                                     }})
        return True

    def updateTopic(self,json_data):
        topic_id = json_data['topic_id']
        topic = json_data['topic']
        # news_id = json_data['news']
        topic_desc = json_data['topic_desc']
        res = db.topic.find_one({'topic_id': topic_id})
        if res is None: return False

        db.topic.update_one({'topic_id': topic_id},
                            {'$set': {'topic': topic, 'topic_desc': topic_desc
                                      }})
        return True

    def addTopic(self,json_data):
        topic_id = json_data['topic_id']
        topic = json_data['topic']
        topic_desc = json_data['topic_desc']
        db.topic.insert_one({
            'topic_id': topic_id, 'topic': topic, 'topic_desc': topic_desc
        })