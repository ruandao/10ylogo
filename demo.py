from PIL import Image,ImageDraw,ImageFont
import time
import os

sourceimg = "/Users/weixin/Desktop/a.png"
savepath = "/Users/weixin/gitClone/10ylogo/img/"
fontPath = "/Users/weixin/Desktop/Font/Fonts/simsun.ttc"
def imgaddnum(img):
    # 将img添加到画板
    imgdraw = ImageDraw.Draw(img)
    # 设置需要绘制的字体 参数：字体名，字体大小
    imgfont = ImageFont.truetype("Arial", size=30)
    imgfont = ImageFont.truetype(fontPath, size=30)

    # 字体颜色
    fillcolor = "#dd1c5c"
    # 获取img的宽和高
    imgw,imgh = img.size
    # 开始将文字内容绘制到img的画板上 参数：坐标，绘制内容，填充颜色，字体
    imgdraw.text((imgw/2,0),"你好时间",fill=fillcolor,font=imgfont)
    # 设置img的保存路径和文件名
    imgsavetarget = savepath + "abc" + time.strftime("%Y%m%d%H%M%S") + ".png"
    # 开始保存
    res = img.save(imgsavetarget, "png")
    # 返回保存结果
    return res

# 初始化一个img对象 为None
targetimg = None
# 判断需要打开的img对象路径是否存在
if os.path.exists(sourceimg):
    targetimg = Image.open(sourceimg)
    rig = imgaddnum(targetimg)
    print(rig)
else:
    print("Image Not Found!")
