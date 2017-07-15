
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack , make_response

from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

import urllib, cStringIO
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from add_watermark import add_text_to_image

import reply , urllib2 , json , requests , StringIO

token = 'xjj'
appId = 'wx0bf5a881e5a22886'
appSecret = 'a301e26f45585c26823d24be7a4b2fda'
getTokenResult = urllib2.urlopen( r'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appId + '&secret=' + appSecret )
tokenJson = json.loads( getTokenResult.read( ) )
access_token = tokenJson['access_token']

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/weixin' , methods=['GET','POST'])
def weixin( ) :
    import hashlib , lxml , time , os , urllib2 , json 
    from lxml import etree
    if request.method == 'GET' :
        signature =	request.values.get( 'signature' )
        timestamp =	request.values.get( 'timestamp' )
        nonce =		request.values.get( 'nonce' )
        echostr =	request.values.get( 'echostr' )
        token = 'xjj'		
        list = [ token , timestamp , nonce ]
        list.sort( )
        sha1 = hashlib.sha1( )
        map( sha1.update , list )
        hashcode = sha1.hexdigest( )
        if hashcode == signature :
            return echostr
        else :
            return echostr+'failed'
    elif request.method == 'POST' :
        str_xml = request.data
        xml = etree.fromstring( str_xml )
        msgType = 	xml.find( "MsgType" ).text
        fromUser = 	xml.find( "FromUserName" ).text
        toUser = 	xml.find( "ToUserName" ).text
        print( str_xml )
        if msgType == 'text' :
            content = 	xml.find( "Content" ).text
            values = [
                { 'toUser':fromUser , 'fromUser':toUser , 'createTime':int( time.time( ) ) , 'content' : u'u just say : ' + content },
            ]
            template = render_template( 'reply_text.xml' , values = values )
            response = make_response( template )
            response.headers['Content-Type'] = 'application/xml'
            return response
        elif msgType == 'image' :
            PicUrl = xml.find( "PicUrl" ).text
            watermark = "marked at " + str(datetime.now()) + "\nby qiyunhu@gxxd"
            im_before = Image.open(cStringIO.StringIO(urllib.urlopen(PicUrl).read()))
            icc_profile = im_before.info.get("icc_profile")
            im_after = add_text_to_image(im_before, watermark,fill=(255,255,255,255))
            im_after = add_text_to_image(im_after, watermark,fill=(0,0,0,255),ray=1)
            sio = StringIO.StringIO( )
            im_after.save( sio , format='jpeg' , icc_profile=icc_profile )
            files = { 'media' : ( 'temp.jpg' , sio.getvalue() ) }
            upload_url="https://api.weixin.qq.com/cgi-bin/media/upload?access_token=" + access_token + "&type=image" # set your access_token
            r=requests.post(upload_url, files=files) # upload 
            media_id=json.loads(r.content)['media_id']
            replyMsg = reply.ImageMsg( fromUser , toUser , media_id )
            return replyMsg.send( )
    return 'wassup'

if __name__ == '__main__':
    app.run(host="10.135.22.157",port=80)
