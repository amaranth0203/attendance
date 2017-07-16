
# -*- coding: utf-8 -*-

import io , urllib , json , requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from wechatpy import WeChatClient

class add_watermark( object ) :
    watermark = "marked at " + str(datetime.now()) + "\nby qiyunhu@gxxd"
    def __init__( self , media_id , app_id , app_secret ) :
        self.media_id = media_id
        self.app_id = app_id
        self.app_secret = app_secret
        self.font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', size=44)
        self.access_token = json.loads( 
            urllib.request.urlopen( 
                r'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + self.app_id + '&secret=' + self.app_secret 
            ).read( ).decode( 'utf-8' ) )['access_token']
        self.media_id_after = None
        self.process( )
    def add_text_to_image( self , image , text , fill=(0,0,0,180) , ray=0 ) :
        rgba_image = image.convert('RGBA')
        text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
        image_draw = ImageDraw.Draw(text_overlay)
        text_size_x, text_size_y = image_draw.textsize(text,font=self.font)
        text_xy = (rgba_image.size[0] - text_size_x, rgba_image.size[1] - text_size_y * (1.3+ray))
        image_draw.multiline_text(text_xy, text, font=self.font,fill=fill,align='right')
        image_with_text = Image.alpha_composite(rgba_image, text_overlay)
        image_with_text = image_with_text.convert('RGB')
        return image_with_text
    def process( self ) :
        client = WeChatClient( self.app_id , self.app_secret )
        pic_url = client.media.get_url( self.media_id )
        im_before = Image.open( io.BytesIO( urllib.request.urlopen( pic_url ).read( ) ) )
        icc_profile = im_before.info.get( "icc_profile" )
        im_after = self.add_text_to_image( im_before , self.watermark , fill = ( 255 , 255 , 255 , 255 ) )
        im_after = self.add_text_to_image( im_after , self.watermark , fill = ( 0 , 0 , 0 , 255 ) , ray = 1 )
        bio = io.BytesIO( )
        im_after.save( bio , format='jpeg' , icc_profile = icc_profile )
        files = { 'media' : ( 'temp.jpg' , bio.getvalue( ) ) }
        upload_url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=" + self.access_token + "&type=image"
        r = requests.post( upload_url , files=files ) # upload 
        self.media_id_after = json.loads( r.content.decode('utf-8') )['media_id']
    def get_media_id_with_watermark( self ) :
        return self.media_id_after
