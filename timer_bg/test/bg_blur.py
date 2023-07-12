import os
import requests
from datetime import datetime
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import ctypes

def circle_corner(img, radii):
    # 画圆（用于分离4个角）
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形
    # 原图
    img = img.convert("RGBA")
    w, h = img.size
    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
    # alpha.show()
    img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
    return img

# 下载壁纸
# response = requests.get("https://bing.shangzhenyang.com/api/1080p")
# with open("wallpaper.jpg", "wb") as file:
#     file.write(response.content)

# 计算日期差
today = datetime.now()
target_date = datetime.strptime("2026-6-7", "%Y-%m-%d")  # 请将此处的 YYYY-MM-DD 替换为目标日期
delta = (target_date - today).days

# 处理图片
image = Image.open("wallpaper.jpg")
draw = ImageDraw.Draw(image)
blur_rect_radius = 200
blur_rect_width = 500
blur_rect_height = 300

# 添加模糊图层
box = (image.width // 2 - blur_rect_width // 2, image.height // 2 - blur_rect_height // 2, image.width // 2 + blur_rect_width //2, image.height // 2 + blur_rect_height // 2)
blur_image = image.copy().filter(ImageFilter.GaussianBlur(10)).crop((box))
blur_image = circle_corner(blur_image,blur_rect_radius)
#mask = Image.new('L', (blur_rect_width, blur_rect_height), 256).resize((blur_rect_width + blur_rect_radius, blur_rect_height + blur_rect_radius)).crop((blur_rect_radius // 2, blur_rect_radius // 2, blur_rect_width + blur_rect_radius // 2, blur_rect_height + blur_rect_radius // 2))
#image.paste(blur_image, box, mask)
r, g, b, a = blur_image.split()
image.paste(blur_image,box,mask=a)

# 添加文字
unifont = ImageFont.truetype('unifont.ttf', 50)  # 请确保 unifont.ttf 字体文件在当前目录下
draw.text((image.width // 2, image.height // 2 - 40), "倒计时", font=unifont, fill="#ffffff", anchor="mm")
draw.text((image.width // 2, image.height // 2), str(delta), font=unifont, fill="#ffffff", anchor="mm")
draw.text((image.width // 2 + 100, image.height // 2), "天", font=unifont, fill="#ffffff", anchor="mm")

# 保存图片
image.save("processed_wallpaper.png")
#blur_image.save("test.png")
# 设置为系统背景
#ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath("processed_wallpaper.jpg"), 3)

