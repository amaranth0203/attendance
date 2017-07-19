
# -*- coding: utf-8 -*-
from flask import Flask, request

from wechatpy import WeChatClient , parse_message
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import TextReply , ImageReply

from toolkit import add_watermark

token = 'xjj'
appId = 'wx0bf5a881e5a22886'
appSecret = 'a301e26f45585c26823d24be7a4b2fda'
application = Flask(__name__)
client = WeChatClient( appId , appSecret )

@application.route('/weixin' , methods=['GET','POST'])
def weixin( ) :
    import hashlib , lxml , time , os , json 
    from lxml import etree
    if request.method == 'GET' :
        signature =	request.values.get( 'signature' )
        timestamp =	request.values.get( 'timestamp' )
        nonce =		request.values.get( 'nonce' )
        echostr =	request.values.get( 'echostr' )
        global token
        try :
            check_signature( 
                token , 
                signature , 
                timestamp , 
                nonce 
            )
            return echostr
        except InvalidSignatureException : 
            return echostr + 'failed'
    elif request.method == 'POST' :
        str_xml = request.data
        msg = parse_message( str_xml )
        print( str_xml )
        if msg.type == 'text' :
            return TextReply( 
                content = 'u just say : ' + msg.content , 
                message = msg 
            ).render( )
        elif msg.type == 'image' :
            return ImageReply( 
                media_id = add_watermark(
                    msg.media_id ,
                    appId ,
                    appSecret
                ).get_media_id_with_watermark( ) , 
                message = msg 
            ).render( )
    return 'wassup'

@application.route('/')
def hello( ) :
    return 'wassup in index'

@application.route('/mini' , methods=['GET','POST'])
def mini( ) :
    if request.method == 'POST' :
        print( request.data )
    return 'function mini return \'wassup\''

if __name__ == '__main__':
    application.run(
        host = "10.135.22.157" ,
#        host = '127.0.0.1' , 
        port = 443 ,
        ssl_context = 'adhoc'
    )
