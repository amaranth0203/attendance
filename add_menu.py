#-*- coding:utf-8 -*-
from wechatpy import WeChatClient

appId = 'wx0bf5a881e5a22886'
appSecret = 'a301e26f45585c26823d24be7a4b2fda'

client = WeChatClient(appId,appSecret)
print( client.menu.create({
    "button":[
        {
            "type":"pic_sysphoto",
            "name":"拍照测试  拍照测试",
            "key":"V1001_TODAY_MUSIC"
        }
    ]
})
)
