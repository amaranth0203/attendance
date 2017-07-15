from time import gmtime, strftime
from datetime import datetime
import urllib , cStringIO
from PIL import Image, ImageDraw, ImageFont
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', size=44)
def add_text_to_image(image, text , font=font , fill=(0,0,0,180),ray=0):
    rgba_image = image.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    text_size_x, text_size_y = image_draw.textsize(text,font=font)
    text_xy = (rgba_image.size[0] - text_size_x, rgba_image.size[1] - text_size_y * (1.3+ray))
    image_draw.multiline_text(text_xy, text, font=font,fill=fill,align='right')
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)
    image_with_text = image_with_text.convert('RGB')
    return image_with_text
 
URL="http://mmbiz.qpic.cn/mmbiz_jpg/QcRDBAkcU7YOEejyOb51pSdug51k3W3V4eZtNy9UH1tFibdJpjhIhGCLgEMSRJbvibukQrjqHhJqibTToMpY655tA/0"
watermark = "marked at "+str(datetime.now())+"\nby qiyunhu@gxxd"
'''
im_before = Image.open(cStringIO.StringIO(urllib.urlopen(URL).read()))
icc_profile = im_before.info.get("icc_profile")
im_after = add_text_to_image(im_before, watermark,fill=(255,255,255,255))
im_after = add_text_to_image(im_after, watermark,fill=(0,0,0,255),ray=1)
im_after.save('ttttt.jpg',icc_profile=icc_profile)
'''
