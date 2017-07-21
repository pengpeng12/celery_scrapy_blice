#/usr/lib64/python
#coding=utf-8

movieUrls = \
{   "全部":["http://v.qq.com/x/list/movie?area=-1&cate=-1&sort=5&offset=%s&pay=-1"%i for i in range(0,5130,30)],
    "网络电影":["http://v.qq.com/x/list/movie?area=-1&sort=5&offset=%s&pay=-1&cate=10006"%i for i in range(0,2100,30)],
    "动作":["http://v.qq.com/x/list/movie?area=-1&offset=%s&pay=-1&subtype=100061&sort=5" %i for i in range(0,4200,30)],
    "冒险":["http://v.qq.com/x/list/movie?subtype=100003&area=-1&pay=-1&sort=5&offset=%s" %i for i in range(0,2100,30)],
    "喜剧":["http://v.qq.com/x/list/movie?area=-1&subtype=100004&sort=5&offset=%s&pay=-1" %i for i in range(0,6000,30)],
    "爱情":["http://v.qq.com/x/list/movie?subtype=100005&area=-1&pay=-1&sort=5&offset=%s" %i for i in range(0,6000,30)],
    "战争":["http://v.qq.com/x/list/movie?area=-1&subtype=100006&pay=-1&offset=%s&sort=5" %i for i in range(0,1140,30)],
    "恐怖":["http://v.qq.com/x/list/movie?pay=-1&area=-1&offset=%s&sort=5&subtype=100007" %i for i in range(0,2100,30)],
    "犯罪":["http://v.qq.com/x/list/movie?area=-1&offset=%s&subtype=100008&pay=-1&sort=5" %i for i in range(0,2100,30)],
    "悬疑":["http://v.qq.com/x/list/movie?subtype=100009&area=-1&pay=-1&sort=5&offset=%s" %i for i in range(0,2400,30)],
    "惊悚":["http://v.qq.com/x/list/movie?area=-1&subtype=100010&sort=5&offset=%s&pay=-1" %i for i in range(0,3600,30)],
    "武侠":["http://v.qq.com/x/list/movie?pay=-1&area=-1&sort=5&offset=%s&subtype=100011" %i for i in range(0,600,30)],
    "科幻":["http://v.qq.com/x/list/movie?pay=-1&area=-1&sort=5&offset=%s&subtype=100012" %i for i in range(0,1500,30)],
    "音乐":["http://v.qq.com/x/list/movie?area=-1&subtype=100013&sort=5&offset=%s&pay=-1" %i for i in range(0,900,30)],
    "歌舞":["http://v.qq.com/x/list/movie?offset=%s&area=-1&pay=-1&subtype=100014&sort=5" %i for i in range(0,600,30)],
    "动画":["http://v.qq.com/x/list/movie?pay=-1&area=-1&offset=%s&sort=5&subtype=100015" %i for i in range(0,2100,30)],
    "奇幻":["http://v.qq.com/x/list/movie?area=-1&sort=5&subtype=100016&offset=%s&pay=-1" %i for i in range(0,1800,30)],
    "家庭":["http://v.qq.com/x/list/movie?subtype=100017&area=-1&pay=-1&sort=5&offset=%s" %i for i in range(0,2400,30)],
    "剧情":["http://v.qq.com/x/list/movie?pay=-1&area=-1&sort=5&offset=%s&subtype=100018" %i for i in range(0,6000,30)],
    "伦理":["http://v.qq.com/x/list/movie?pay=-1&area=-1&sort=5&offset=%s&subtype=100019" %i for i in range(0,600,30)],
    "记录":["http://v.qq.com/x/list/movie?area=-1&sort=5&offset=%s&subtype=100020&pay=-1" %i for i in range(0,600,30)],
    "历史":["http://v.qq.com/x/list/movie?area=-1&offset=%s&pay=-1&subtype=100021&sort=5" %i for i in range(0,900,30)],
    "传记":["http://v.qq.com/x/list/movie?sort=5&area=-1&pay=-1&subtype=100022&offset=%s" %i for i in range(0,900,30)],
    "院线":["http://v.qq.com/x/list/movie?subtype=100062&area=-1&pay=-1&sort=5&offset=%s" %i for i in range(0,2400,30)]
}





TVurls =\
    {
        "全部":["http://v.qq.com/x/list/tv?offset=%s&sort=5" %i for i in range(0,6000,30)],
        "偶像":["http://v.qq.com/x/list/tv?sort=5&offset=%s&itype=820" %i for i in range(0,600,30)],
        "喜剧":["http://v.qq.com/x/list/tv?offset=%s&itype=821&sort=5" %i for i in range(0,500,30)],
        "爱情":["http://v.qq.com/x/list/tv?offset=%s&itype=822&sort=5"%i for i in range(0,900,30)],
        "都市":["http://v.qq.com/x/list/tv?offset=%s&itype=823&sort=5"%i for i in range(0,300,30)],
        "古装":["http://v.qq.com/x/list/tv?itype=824&sort=5&offset=%s" %i for i in range(0,300,30)],
        "武侠":["http://v.qq.com/x/list/tv?offset=%s&itype=825&sort=5" %i for i in range(0,150,30)],
        "历史":["http://v.qq.com/x/list/tv?offset=%s&sort=5&itype=826" %i for i in range(0,210,30)],
        "警匪":["http://v.qq.com/x/list/tv?offset=%s&itype=827&sort=5" %i for i in range(0,150,30)],
        "家庭":["http://v.qq.com/x/list/tv?sort=5&itype=828&offset=%s" %i for i in range(0,600,30)],
        "神话":["http://v.qq.com/x/list/tv?sort=5&offset=%s&itype=829" %i for i in range(0,120,30)],
        "剧情":["http://v.qq.com/x/list/tv?offset=%s&itype=830&sort=5"  %i for i in range(0,1200,30)],
        "悬疑":["http://v.qq.com/x/list/tv?sort=5&itype=831&offset=%s" %i for i in range(0,420,30)],
        "战争":["http://v.qq.com/x/list/tv?itype=832&offset=%s&sort=5" %i for i in range(0,300,30)],
        "军事":["http://v.qq.com/x/list/tv?itype=833&sort=5&offset=%s" %i for i in range(0,120,30)],
        "犯罪":["http://v.qq.com/x/list/tv?offset=%s&sort=5&itype=834" %i for i in range(0,300,30)],
        "情景":["http://v.qq.com/x/list/tv?offset=%s&itype=835&sort=5" %i for i in range(0,120,30)],
        "谍战":["http://v.qq.com/x/list/tv?offset=%s&itype=836&sort=5"  %i for i in range(0,120,30)],
        "片花":["http://v.qq.com/x/list/tv?itype=837&offset=%s&sort=5" %i for i in range(0,600,30)],
        "魔幻":["http://v.qq.com/x/list/tv?sort=5&offset=%s&itype=838" %i for i in range(0,120,30)],
        "动作":["http://v.qq.com/x/list/tv?offset=%s&itype=839&sort=5" %i for i in range(0,300,30)],
        "科幻":["http://v.qq.com/x/list/tv?itype=840&sort=5&offset=%s" %i for i in range(0,300,30)],
        "刑侦":["http://v.qq.com/x/list/tv?sort=5&itype=841&offset=%s" %i for i in range(0,120,30)],
        "恐怖":["http://v.qq.com/x/list/tv?sort=5&offset=%s&itype=842" %i for i in range(0,120,30)],
        "自制剧":["http://v.qq.com/x/list/tv?itype=843&offset=%s&sort=5" %i for i in range(0,120,30)],
        "网络剧":["http://v.qq.com/x/list/tv?sort=5&offset=%s&itype=844" %i for i in range(0,600,30)]
    }

showUrls = \
    {   "全部":["http://v.qq.com/x/list/variety?sort=5&offset=%s" %i for i in range(0,1500,30)],
        "真人秀":["http://v.qq.com/x/list/variety?offset=%s&sort=5&itype=163223" %i for i in range(0,600,30)],
        "情感":["http://v.qq.com/x/list/variety?offset=%s&sort=5&itype=97215" %i for i in range(0,120,30)],
        "访谈":["http://v.qq.com/x/list/variety?sort=5&offset=%s&itype=97210" %i for i in range(0,210,30)],
        "音乐":["http://v.qq.com/x/list/variety?itype=216997&sort=5&offset=%s" %i for i in range(0,600,30)],
        "美食":["http://v.qq.com/x/list/variety?itype=97989&sort=5&offset=%s" %i for i in range(0,120,30)],
        "旅游":["http://v.qq.com/x/list/variety?offset=%s&sort=5&itype=97987" %i for i in range(0,150,30)],
        "竞技":["http://v.qq.com/x/list/variety?offset=%s&sort=5&itype=216966" %i for i in range(0,150,30)],
        "亲子":["http://v.qq.com/x/list/variety?itype=164939&offset=%s&sort=5" %i for i in range(0,150,30)],

        "脱口秀":["http://v.qq.com/x/list/variety?sort=5&itype=97217&offset=%s" %i for i in range(0,300,30)],
        "选秀":["http://v.qq.com/x/list/variety?itype=97991&sort=5&offset=%s" %i for i in range(0,300,30)],
        "纪实":["http://v.qq.com/x/list/variety?itype=97274&sort=5&offset=%s" %i for i in range(0,180,30)],
        "其他":["http://v.qq.com/x/list/variety?sort=5&offset=%s&itype=9999" %i for i in range(0,900,30)]
    }

rankUrls= {"电影":{"全部":{"日榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_2_-1.html",
                            "周榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_3_-1.html",
                            "月榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_4_-1.html",
                            "总榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_1_-1.html"},
                    "内地":{"日榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_2_1.html",
                            "周榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_3_1.html",
                            "月榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_4_1.html",
                            "总榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_1_1.html"},
                    "香港":{"日榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_2_2.html",
                            "周榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_3_2.html",
                            "月榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_4_2.html",
                            "总榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_1_2.html"},
                     "美国":{"日榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_2_3.html",
                            "周榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_3_3.html",
                            "月榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_4_3.html",
                            "总榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_1_3.html"},
                     "欧洲":{"日榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_2_4.html",
                            "周榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_3_4.html",
                            "月榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_4_4.html",
                            "总榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_1_4.html"},
                      "其他":{"日榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_2_9999.html",
                            "周榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_3_9999.html",
                            "月榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_4_9999.html",
                            "总榜":"http://v.qq.com/rank/detail/1_-1_-1_-1_1_9999.html"}},
            "电视剧":{"全部":{"日榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_2_-1.html",
                            "周榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_3_-1.html",
                            "月榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_4_-1.html",
                            "总榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_1_-1.html"},
                       "内地":{"日榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_2_1.html",
                            "周榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_3_1.html",
                            "月榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_4_1.html",
                            "总榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_1_1.html"},
                       "香港":{"日榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_2_2.html",
                            "周榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_3_2.html",
                            "月榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_4_2.html",
                            "总榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_1_2.html"},
                       "台湾":{"日榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_2_3.html",
                            "周榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_3_3.html",
                            "月榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_4_3.html",
                            "总榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_1_3.html"},
                       "韩国":{"日榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_2_4.html",
                            "周榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_3_4.html",
                            "月榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_4_4.html",
                            "总榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_1_4.html"},
                       "其他":{"日榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_2_9999.html",
                            "周榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_3_9999.html",
                            "月榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_4_9999.html",
                            "总榜":"http://v.qq.com/rank/detail/2_-1_-1_-1_1_9999.html"}},
            "动漫":{"日榜":"http://v.qq.com/rank/detail/3_-1_-1_-1_2_-1.html",
                    "周榜":"http://v.qq.com/rank/detail/3_-1_-1_-1_3_-1.html",
                    "月榜":"http://v.qq.com/rank/detail/3_-1_-1_-1_4_-1.html",
                    "总榜":"http://v.qq.com/rank/detail/3_-1_-1_-1_1_-1.html"},
            "综艺":{"日榜":"http://v.qq.com/rank/detail/10_-1_-1_-1_2_-1.html",
                            "周榜":"http://v.qq.com/rank/detail/10_-1_-1_-1_3_-1.html",
                            "月榜":"http://v.qq.com/rank/detail/10_-1_-1_-1_4_-1.html",
                            "总榜":"http://v.qq.com/rank/detail/10_-1_-1_-1_1_-1.html"}}



# for nameUrlList in movieUrls.items():
#     print nameUrlList[1]
#     import time
#     time.sleep(20)

