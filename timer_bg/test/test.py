from PIL import Image

# 加载图像
img = Image.open('image.jpg')

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

# 显示图像
img_cropped.show()
