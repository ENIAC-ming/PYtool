from PIL import Image, ImageDraw, ImageFont
from requests import get
from io import BytesIO
import ctypes
from datetime import datetime, timedelta
import os

def rerad(img):
    # 计算裁剪区域
    aspect_ratio = 16 / 9
    width, height = img.size
    new_width = width
    new_height = int(new_width / aspect_ratio)

    if new_height > height:
        new_height = height
        new_width = int(new_height * aspect_ratio)

    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = left + new_width
    bottom = top + new_height

    # 裁剪图像
    img_cropped = img.crop((left, top, right, bottom))
    return img_cropped.resize((1920,1080))

def get_font(size):
    if os.path.exists('unifont.ttf'):
        font = ImageFont.truetype('unifont.ttf', size=size) 
    else:
        try:
            response = get('https://www.unifoundry.com/pub/unifont/unifont-15.0.06/font-builds/unifont-15.0.06.ttf')
            with open('unifont.ttf', 'wb') as f:
                f.write(response.content)
            font = ImageFont.truetype('unifont.ttf', size=size) 
        except:
            font = ImageFont.truetype('C:\\Windows\\Fonts\\simhei.ttf', size=size)
    return font

# 指定日期
target_date = datetime(2026, 6, 7)

# 计算天数
days_left = (target_date - datetime.now()+timedelta(days=1)).days

# 下载壁纸
if os.path.exists('bg.png'): img_path = 'bg.png'
elif os.path.exists('bg.jpg'): img_path = 'bg.jpg'
elif os.path.exists('bg.bmp'): img_path = 'bg.bmp'
else:
    try:
        response = get('https://bing.shangzhenyang.com/api/1080p')
        with open('bing.jpg', 'wb') as f:
            f.write(response.content)
    except:
        Image.new('RGB', (1920,1080), 0).save('bing.jpg')
    img_path = 'bing.jpg'
img = rerad(Image.open(img_path))

# 处理图像
draw = ImageDraw.Draw(img)
width, height = img.size

# 添加图层
overlay = Image.new('RGBA', img.size, (0, 0, 0, 128))
img.paste(overlay, (0, 0), overlay)

font = get_font(100)
text = f'{days_left:04d}'
x,x,text_width, text_height = font.getbbox(text)
draw.text(((width - text_width) / 2 + 25, (height - text_height) / 2 - 20), text, fill='red', font=font)

font = get_font(50)
text = '距离2026高考'
x,x,text_width, text_height = font.getbbox(text)
draw.text(((width - text_width) / 2, (height - text_height) / 2 - 100), text, fill='white', font=font)

text = '还有'
x,x,text_width, text_height = font.getbbox(text)
draw.text(((width - text_width) / 2 - 150 + 25, (height - text_height) / 2), text, fill='white', font=font)

text = '天'
x,x,text_width, text_height = font.getbbox(text)
draw.text(((width - text_width) / 2 + 125 + 25, (height - text_height) / 2), text, fill='white', font=font)

# 设置壁纸
img.save('wallpaper.bmp')
ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(os.getcwd(),'wallpaper.bmp'), 0)