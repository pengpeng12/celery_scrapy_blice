# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BookItem(Item):
    MysqlBookTable_name = 'fiction_info'

    genderType = Field()
    genderTypeId = Field()
    # 小说类型vc_class
    categoryType = Field()
    categoryTypeId = Field()
    # 是否连载中serialstatus  0连载中 1 已完结
    # serialstatus = Field()

    # 小说唯一id   vc_infoid
    bid = Field()
    bname = Field()
    bookIcon = Field()
    author = Field()
    # 连载中/完结
    vc_tags = Field()
    # 标签|分隔
    vc_label = Field()
    stringNumber = Field()

    bookIntro = Field()
    # 小说url
    vc_url = Field()

    # 月推荐
    monthRecommend = Field()
    # 月点击
    monthTouch = Field()
    # 总点击
    totalTouch = Field()
    # 总收藏
    totalCollection = Field()
    # 总推荐
    totalRecommend = Field()
    # 评论数
    discussCount = Field()

    dt_create = Field()
    dt_update = Field()


class CommentItem(Item):
    MysqlCommentTable_name = 'fuction_comment'

    # 小说name
    vc_name = Field()
    # 小说唯一id
    vc_infoid = Field()
    # 小说的url
    vc_url = Field()

    vc_userName = Field()
    vc_userImg = Field()
    vc_userId = Field()
    # 评论发布时间
    vc_public = Field()
    # 总点击
    nm_click = Field()
    # 评论赞
    nm_up = Field()
    # 回复
    nm_reply = Field()
    # 评论内容
    vc_content = Field()

    dt_create = Field()
    dt_update = Field()