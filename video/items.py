# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoItem(scrapy.Item):
    '''
    短视频item
    '''
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field()  # 标题
    author = scrapy.Field()  # 名称
    channel = scrapy.Field()  # 渠道
    sub_title = scrapy.Field()  # 副标题
    video_url = scrapy.Field()  # 图片地址
    tags = scrapy.Field()  # 标签
    description = scrapy.Field()  # 描述
    words = scrapy.Field()  # 搜索关键词
    published_at = scrapy.Field()  # 发表时间
    url = scrapy.Field()  # 地址
    love_count = scrapy.Field()  # 点赞数
    view_count = scrapy.Field()  # 浏览数
    comment_count = scrapy.Field()  # 评论数
