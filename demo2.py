import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

iconpath = "/Users/weixin/gitClone/10ylogo/icon/earphone.png"
savepath = "/Users/weixin/gitClone/10ylogo/img/"
fontPath = "/Users/weixin/Desktop/Font/Fonts/simsun.ttc"

iconImg = Image.open(iconpath, 'r')

font = ImageFont.truetype(fontPath,25)
img=Image.new("RGBA", (200,200),(255,255,255))
img.paste(iconImg, (0,0))
draw = ImageDraw.Draw(img)
draw.text((10, 10),"This is a test",(0,0,0),font=font)
draw = ImageDraw.Draw(img)
img.save(savepath + "demo2.png")