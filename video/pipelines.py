# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#
from pymongo import MongoClient
from requests.adapters import HTTPAdapter
from scrapy.utils.project import get_project_settings

from video.settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME, SHEETE_NAME
import random
import requests
import json
import base64
from io import BytesIO
import time
import os


class VideoSavePipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        pass

    def close_spider(self, spider):
        pass
