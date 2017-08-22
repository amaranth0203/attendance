
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify , render_template

from wechatpy import WeChatClient , parse_message
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import TextReply , ImageReply

from toolkit import add_watermark
from db_ops import *

import urllib.request
import urllib.parse

token = 'xjj'
appId = 'wx0bf5a881e5a22886'
appSecret = 'a301e26f45585c26823d24be7a4b2fda'
application = Flask(__name__)
client = WeChatClient( appId , appSecret )

mini_app_id = 'wxc41ab2f0498e2894'
mini_app_secret = '3d0d8ef0085a0d05202536bacc70dd87'

def get_openid( jscode ) :
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code'
    return json.loads(
        urllib.request.urlopen(
            url.replace( 'APPID' , mini_app_id ).replace( 'SECRET' , mini_app_secret ).replace( 'JSCODE' , jscode )
        ).read( ).decode( 'utf-8' )
    )['openid']

def get_access_token( ) :
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET'
    return json.loads(
        urllib.request.urlopen(
            url.replace( 'APPID' , mini_app_id ).replace( 'APPSECRET' , mini_app_secret )
        ).read( ).decode( 'utf-8' )
    )['access_token']

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
    return render_template( 'test_pengyouquan.html' )
    return 'wassup in index'

@application.route('/mini/test' , methods=['POST'])
def mini_test( ) :
    #
    # if openid exists, return user info
    # if openid not exists , go to login
    #
    data = { 
        'result' : '' ,
        'reason' : '' ,
    }
    if request.method == 'POST' :
        url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=ACCESS_TOKEN'
        url = url.replace( 'ACCESS_TOKEN' , get_access_token( ) )
        print( request.data )
        request_to_send = urllib.request.Request(
            url ,
            urllib.parse.urlencode(
                {
                    "touser": "oZqgd0RuyGvRb5zASsiw21SY8C9E",
                    "template_id": "M3zLARKl-kk6UDqqUq1rzewTApIAeb5MJAn58gZSuas",
                    "page": request.get_json( )['page'],
                    "form_id": request.get_json( )['form_id'],
                    "data": request.get_json( )['value']
                }
            ).encode()
        )
        print( '-----------------------------------------' )
        print( urllib.request.urlopen( request_to_send ).read( ).decode( ) )
        print( '-----------------------------------------' )
    return 'function mini_index return \'wassup\''

@application.route('/mini/location' , methods=['POST'])
def mini_location( ) :
    if request.method == 'POST' :
        print( request.data )
    return 'function mini_location return \'wassup\''

@application.route('/mini/students_info' , methods=['POST'])
def mini_students_info( ) :
    #
    # if openid exists, return user info
    # if openid not exists , go to login
    #
    data = { 
        'result' : '' ,
        'reason' : '' ,
        'data' : ''
    }
    if request.method == 'POST' :
        openid = get_openid( request.get_json( )['jscode'] )
        if db_check_openid( openid ) == False :
            data['result'] = 'failed'
            data['reason'] = 'openid not exists'
        else :
            data['result'] = 'success'
            data['data'] = db_get_students_info_by_teacher_openid( openid )
        return jsonify( data )
    return 'function mini_students_info return \'wassup\''

@application.route('/mini/teacher' , methods=['POST'])
def mini_teacher( ) :
    #
    # if openid exists, return user info
    # if openid not exists , go to login
    #
    data = { 
        'result' : '' ,
        'reason' : '' ,
        'data' : ''
    }
    if request.method == 'POST' :
        openid = get_openid( request.get_json( )['jscode'] )
        if db_check_openid( openid ) == False :
            data['result'] = 'failed'
            data['reason'] = 'openid not exists'
        else :
            data['result'] = 'success'
            data['data'] = db_get_teacher_info( openid )
        return jsonify( data )
    return 'function mini_teacher return \'wassup\''

@application.route('/mini/index' , methods=['POST'])
def mini_index( ) :
    #
    # if openid exists, return user info
    # if openid not exists , go to login
    #
    data = { 
        'result' : '' ,
        'reason' : '' ,
        'data' : ''
    }
    if request.method == 'POST' :
        openid = get_openid( request.get_json( )['jscode'] )
        if db_check_openid( openid ) == False :
            data['result'] = 'failed'
            data['reason'] = 'openid not exists'
        else :
            data['result'] = 'success'
            data['data'] = db_get_wechat_info( openid )
        return jsonify( data )
    return 'function mini_index return \'wassup\''

@application.route( '/mini/login' , methods=['POST'] )
def mini_login( ) :
    #
    # username
    # passwd
    # wechat.openid
    #
    # if( check_user( username , passwd ) ) :
    #   add( username , passwd , wechatid )
    #   return True
    # else :
    #   return False
    data = { 
        'result' : '' , # 'success' 'failed'
        'reason' : '' , # 'password_error' 'unkonw_user'
    }
    if request.method == 'POST' :
        print( request.data )
        
        rc = db_check_user_and_add_openid(
                request.get_json( )['username'] ,
                request.get_json( )['password'] ,
                get_openid( request.get_json( )['jscode'] )
        )
        print( 'rc = %s' % rc )
        if rc == 'success' :
            data['result'] = 'success'
            data['reason'] = 'success'
        elif rc == 'password_error' :
            data['result'] = 'failed'
            data['reason'] = 'password_error'
        elif rc == 'unknow_user' :
            data['result'] = 'failed'
            data['reason'] = 'unknow_user'
        return jsonify( data )
    return 'function mini_login returns'

if __name__ == '__main__':

    exit( 0 )
    application.run(
        host = "10.135.22.157" ,
#        host = '127.0.0.1' , 
        port = 443 ,
        ssl_context = 'adhoc'
    )
