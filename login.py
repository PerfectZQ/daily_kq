# -*- coding:utf-8 -*-

from PIL import Image
import requests
import re
import io
import urllib.parse

from pytesseract import pytesseract


def kq(acc):
    # 保证请求来自同一会话
    session = requests.session()
    response = session.post('http://www.xxxsoft.com/')

    name_pattern = re.compile(r'name="(.*?)"')
    value_pattern = re.compile(r'value="(.*?)"')
    # response.text 返回 string, response.content 返回 raw(bytes-like) object
    names = name_pattern.findall(response.text)
    values = value_pattern.findall(response.text)

    binary_img = session.post('http://www.xxxsoft.com/imageRandeCode')

    img = Image.open(io.BytesIO(binary_img.content))
    img_grey = img.convert('L')

    # 二值化，采用阈值分割法，threshold为分割点
    threshold = 140
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)

    pytesseract.tesseract_cmd = 'D:\\Tesseract-OCR\\tesseract.exe'

    out = img_grey.point(table, '1')

    # 验证码识别
    validate_code = pytesseract.image_to_string(out)
    validate_code = validate_code.strip()
    validate_code = validate_code.upper()
    print('validate_code = %s' % validate_code)
    # 语言包下载 https://github.com/tesseract-ocr/tesseract/wiki/Data-Files
    # 下载后放 $Tesseract_Home\tessdata 目录下
    # now = time.time()
    # validate_code = pytesseract.image_to_string(Image.open('grey_%s.jpg' % now), lang="eng")
    # print(validate_code)

    params = {
        names[1]: values[0],
        names[2]: "",
        names[3]: "",
        names[4]: values[1],
        names[5]: acc['account'],
        names[6]: acc['password'],
        names[7]: validate_code
    }

    params = urllib.parse.urlencode(params)

    headers = {'user-agent': 'mozilla/5.0'}
    # http://www.xxxsoft.com/login_wkq1103_3023.jsp
    # 登陆
    response = session.post("http://www.xxxsoft.com/login.jsp", timeout=30, headers=headers, params=params)
    names = name_pattern.findall(response.text)
    print(names)
    values = value_pattern.findall(response.text)
    print(values)

    params = {names[1]: values[0]}
    params = urllib.parse.urlencode(params)
    # 打卡
    response = session.post("http://www.xxxsoft.com/record.jsp", timeout=30, headers=headers, params=params,
                            allow_redirects=False)
    print(response.text)
    response.raise_for_status()
