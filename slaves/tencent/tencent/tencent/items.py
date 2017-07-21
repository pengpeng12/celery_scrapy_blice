# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy,time
createTime = time.strftime("%Y-%m-%d",time.localtime())
updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())


#腾讯电影的info数据
class TencentItemMovieInfo(scrapy.Item):
    vc_pat = scrapy.Field()
    dt_date = scrapy.Field()
    vc_url = scrapy.Field()
    vc_imgUrl = scrapy.Field()
    is_home = scrapy.Field()
    vc_name = scrapy.Field()
    vc_length = scrapy.Field()
    mc_ao = scrapy.Field()
    sub_mc = scrapy.Field()
    vc_class = scrapy.Field()
    vc_type = scrapy.Field()
    vc_directors = scrapy.Field()
    vc_mainActors = scrapy.Field()
    vc_lag = scrapy.Field()
    vc_act_mc = scrapy.Field()
    vc_area = scrapy.Field()
    vc_detail = scrapy.Field()
    age = scrapy.Field()
    focus = scrapy.Field()
    host = scrapy.Field()
    guest = scrapy.Field()
    by_plat = scrapy.Field()
    vc_label = scrapy.Field()
    vc_tags = scrapy.Field()
    vc_release = scrapy.Field()
    vc_startTime = scrapy.Field()
    vc_endTime = scrapy.Field()
    plat_on = scrapy.Field()
    plat_off = scrapy.Field()
    create_dt = scrapy.Field()
    update_dt = scrapy.Field()
    nm_isVip = scrapy.Field()
    nm_isSelf = scrapy.Field()
    nm_isPay = scrapy.Field()
    nm_isForeshow = scrapy.Field()
    infoid = scrapy.Field()


#腾讯电视剧的info数据
class TencentItemTvInfo(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    imgUrl = scrapy.Field()
    totalType = scrapy.Field()
    year = scrapy.Field()
    area = scrapy.Field()
    lag = scrapy.Field()
    directors = scrapy.Field()
    mainActors = scrapy.Field()
    tags = scrapy.Field()
    zjs = scrapy.Field()
    detail = scrapy.Field()
    isVip = scrapy.Field()
    isSelf = scrapy.Field()
    isPay = scrapy.Field()
    isTencent = scrapy.Field()
    newTags = scrapy.Field()
    bieName = scrapy.Field()
    isNearby = scrapy.Field()
    infoid = scrapy.Field()

#腾讯电影的info数据更新
class TencentItemMovieInfoUpdate(scrapy.Item):
    vc_pat = scrapy.Field()
    dt_date = scrapy.Field()
    vc_url = scrapy.Field()
    vc_imgUrl = scrapy.Field()
    is_home = scrapy.Field()
    vc_name = scrapy.Field()
    vc_length = scrapy.Field()
    mc_ao = scrapy.Field()
    sub_mc = scrapy.Field()
    vc_class = scrapy.Field()
    vc_type = scrapy.Field()
    vc_directors = scrapy.Field()
    vc_mainActors = scrapy.Field()
    vc_lag = scrapy.Field()
    vc_act_mc = scrapy.Field()
    vc_area = scrapy.Field()
    vc_detail = scrapy.Field()
    age = scrapy.Field()
    focus = scrapy.Field()
    host = scrapy.Field()
    guest = scrapy.Field()
    by_plat = scrapy.Field()
    vc_label = scrapy.Field()
    vc_tags = scrapy.Field()
    vc_release = scrapy.Field()
    vc_startTime = scrapy.Field()
    vc_endTime = scrapy.Field()
    plat_on = scrapy.Field()
    plat_off = scrapy.Field()
    create_dt = scrapy.Field()
    update_dt = scrapy.Field()
    nm_isVip = scrapy.Field()
    nm_isSelf = scrapy.Field()
    nm_isPay = scrapy.Field()
    nm_isForeshow = scrapy.Field()
    infoid = scrapy.Field()


#腾讯电视剧的info数据更新
class TencentItemTvInfoUpdate(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    imgUrl = scrapy.Field()
    totalType = scrapy.Field()
    year = scrapy.Field()
    area = scrapy.Field()
    lag = scrapy.Field()
    directors = scrapy.Field()
    mainActors = scrapy.Field()
    tags = scrapy.Field()
    zjs = scrapy.Field()
    detail = scrapy.Field()
    isVip = scrapy.Field()
    isSelf = scrapy.Field()
    isPay = scrapy.Field()
    isTencent = scrapy.Field()
    newTags = scrapy.Field()
    bieName = scrapy.Field()
    isNearby = scrapy.Field()
    infoid = scrapy.Field()

#腾讯综艺的video
class TencentItemVarietyVideo(scrapy.Item):
    titleUrl = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    types = scrapy.Field()
    name = scrapy.Field()
    vclass = scrapy.Field()
    guests = scrapy.Field()
    length = scrapy.Field()
    picUrl = scrapy.Field()
    tags = scrapy.Field()
    year = scrapy.Field()
    presenters = scrapy.Field()
    

#腾讯电影的data数据
class TencentItemMovieData(scrapy.Item):
    v_class = scrapy.Field()
    v_name = scrapy.Field()
    v_url = scrapy.Field()
    v_totalPlayCount = scrapy.Field()
    v_score = scrapy.Field()
    v_todayPlayCount = scrapy.Field()
    v_videoPlayCount = scrapy.Field()
    v_videoTodayPlayCount = scrapy.Field()
    v_tags = scrapy.Field()
    v_date = scrapy.Field()
    v_infoid = scrapy.Field()


#腾讯电视剧data数据
class TencentItemTVData(scrapy.Item):
    v_class = scrapy.Field()
    v_name = scrapy.Field()
    v_url = scrapy.Field()
    v_totalPlayCount = scrapy.Field()
    v_score = scrapy.Field()
    v_todayPlayCount = scrapy.Field()
    v_videoPlayCount = scrapy.Field()
    v_videoTodayPlayCount = scrapy.Field()
    v_tags = scrapy.Field()
    v_date = scrapy.Field()
    v_infoid = scrapy.Field()


#腾讯综艺video数据
class TencentItemVarietyVideo(scrapy.Item):
    v_url = scrapy.Field()
    v_urlInfo = scrapy.Field()
    v_name = scrapy.Field()
    v_type = scrapy.Field()
    v_nameInfo = scrapy.Field()
    v_class = scrapy.Field()
    v_tvYear = scrapy.Field()
    v_imgUrl = scrapy.Field()
    v_presenters = scrapy.Field()
    v_guests = scrapy.Field()
    v_length = scrapy.Field()
    v_date = scrapy.Field()
    v_publishTime = scrapy.Field()
    v_infoid = scrapy.Field()
    v_videoid = scrapy.Field()

#腾讯动漫video数据
class TencentItemCartoonVideo(scrapy.Item):
    v_url = scrapy.Field()
    v_urlInfo = scrapy.Field()
    v_name = scrapy.Field()
    v_type = scrapy.Field()
    v_nameInfo = scrapy.Field()
    v_class = scrapy.Field()
    v_tvYear = scrapy.Field()
    v_imgUrl = scrapy.Field()
    v_presenters = scrapy.Field()
    v_guests = scrapy.Field()
    v_length = scrapy.Field()
    v_date = scrapy.Field()
    v_publishTime = scrapy.Field()
    v_infoid = scrapy.Field()
    v_videoid = scrapy.Field()

#腾讯动漫videodata数据
class TencentItemCartoonVideoData(scrapy.Item):
    v_date = scrapy.Field()
    v_class= scrapy.Field()
    v_name = scrapy.Field()
    v_url = scrapy.Field()
    v_types = scrapy.Field()
    v_playCount = scrapy.Field()
    v_likeCount = scrapy.Field()
    v_unlikeCount = scrapy.Field()
    v_scoreQQ = scrapy.Field()
    v_scoreDB = scrapy.Field()
    v_isVip = scrapy.Field()
    v_isSelf = scrapy.Field()
    v_isPay = scrapy.Field()
    v_videoid = scrapy.Field()


#腾讯综艺videodata数据
class TencentItemVarietyVideoData(scrapy.Item):
    v_date = scrapy.Field()
    v_class= scrapy.Field()
    v_name = scrapy.Field()
    v_url = scrapy.Field()
    v_types = scrapy.Field()
    v_playCount = scrapy.Field()
    v_likeCount = scrapy.Field()
    v_unlikeCount = scrapy.Field()
    v_scoreQQ = scrapy.Field()
    v_scoreDB = scrapy.Field()
    v_isVip = scrapy.Field()
    v_isSelf = scrapy.Field()
    v_isPay = scrapy.Field()
    v_videoid = scrapy.Field()


#腾讯动漫data数据
class TencentItemCartoonData(scrapy.Item):
    vc_class = scrapy.Field()
    vc_name = scrapy.Field()
    vc_url = scrapy.Field()
    totalPlayCount = scrapy.Field()
    score = scrapy.Field()
    todayTotalPlayCount = scrapy.Field()
    videoTotalPlayCount = scrapy.Field()
    todayVideoTotalPlayCount = scrapy.Field()
    tag = scrapy.Field()
    createTime = scrapy.Field()
    infoid = scrapy.Field()

#腾讯电影评论
class TencentItemMovieComment(scrapy.Item):
    content = scrapy.Field()
    commentDate = scrapy.Field()
    region = scrapy.Field()
    url = scrapy.Field()
    userName = scrapy.Field()
    infoid = scrapy.Field()
    name = scrapy.Field()

#腾讯电视剧评论
class TencentItemTVComment(scrapy.Item):
    content = scrapy.Field()
    commentDate = scrapy.Field()
    region = scrapy.Field()
    userName = scrapy.Field()
    url = scrapy.Field()
    videoid = scrapy.Field()
    name = scrapy.Field()


#腾讯综艺评论
class TencentItemVarietyComment(scrapy.Item):
    content = scrapy.Field()
    commentDate = scrapy.Field()
    region = scrapy.Field()
    userName = scrapy.Field()
    url = scrapy.Field()
    videoid = scrapy.Field()
    name = scrapy.Field()


#腾讯动漫评论
class TencentItemCartoonComment(scrapy.Item):
    content = scrapy.Field()
    commentDate = scrapy.Field()
    region = scrapy.Field()
    userName = scrapy.Field()
    url = scrapy.Field()
    videoid = scrapy.Field()
    name = scrapy.Field()









