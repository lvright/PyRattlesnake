# -*- coding: utf-8 -*-

def random_code() -> str:
    """
    随机码生成 6位数字加大小写英文 可用于邀请码、随机命名等
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for _ in range(6)]
    code = ''.join(str_list)
    return code

def code_img() -> dict:
    """
    图像验证码
    """
    # 定义使用Image类实例化一个长为120px,宽为30px,基于RGB的(255,255,255)颜色的图片
    img = Image.new(mode="RGB", size=(120, 30), color=(255, 255, 255))

    # 实例化一支画笔
    draw = ImageDraw.Draw(img, mode="RGB")

    # 定义要使用的字体和字体大小
    font = ImageFont.truetype(font='./static/font/Century751 No2 BT Bold Italic.ttf', size=28)

    # 将每次循环的char存code_text到数组里
    code_text = []

    for i in range(5):
        # 每循环一次,从a到z中随机生成一个字母或数字
        # 65到90为字母的ASCII码,使用chr把生成的ASCII码转换成字符
        # str把生成的数字转换成字符串
        char = random.choice([chr(random.randint(65, 90)), str(random.randint(0, 9))])
        code_text.append(char)
        # 每循环一次重新生成随机颜色
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # 把生成的字母或数字添加到图片上
        # 图片长度为120px,要生成5个数字或字母则每添加一个,其位置就要向后移动24px
        draw.text([i * 24, 0], char, color, font=font)

    # 将code_text数组转字符串
    code = ''.join(code_text)

    file = './static/captcha/' + str(Captcha().random_code()) + '.png'
    filename = file[1:]

    # 保存到本地，推荐保存到云存储
    img.save(file)

    return {'img_code': code, 'img_url': 'http://' + Config.url + ':' + str(Config.port) + filename}