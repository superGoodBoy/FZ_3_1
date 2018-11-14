#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 11:52
# @Author  : QiWei.Ren
# -*- coding: utf-8 -*-
"""
该模块针对防范态势，前端绘制的图来人工判断

"""


from PIL import Image
import sys
def fill_image(image):
    width, height = image.size          #获取原图 长宽度
    print(width, height)
    new_image_length = width if width > height else height
    print(new_image_length)
    # new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
    new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
    if width > height:
        new_image.paste(image, (0, int((new_image_length - height) / 2)))
    else:
        new_image.paste(image, (int((new_image_length - width) / 2), 0))
    return new_image

def cut_image_operator(image,box):
    width, height = image.size
    item_width = int(width / 2)
    box_list = []
    count = 0
    # box1=(668,165,709,179)
    box1=box
    box_list.append(box1)
    print(count)
    image_list = [image.crop(box) for box in box_list]
    return image_list

def cut_image_areatop10(image):
    width, height = image.size
    item_width = int(width / 2)
    box_list = []
    count = 0
    for j in range(0, 2):
        for i in range(0, 2):
            count += 1
            box = (i * item_width, j * item_width, (i + 1) * item_width, (j + 1) * item_width)
            box_list.append(box)
    print(count)
    image_list = [image.crop(box) for box in box_list]
    return image_list

def save_images(image_list,index):

    for image in image_list:
        image.save('result/' + index + '.png')

import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'E:/Tesseract-OCR/tesseract'
def verify(picturename):
    img= Image.open(picturename)
    code=pytesseract.image_to_string(img)
    return code
# keyword=verify(r"F:/python_work/2018_year/windows_path/cmd.png")
# print(keyword)

def get_bin_table(threshold=140):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    return table

def sum_9_region(img, x, y):
    """
    9邻域框,以当前点为中心的田字框,黑点个数
    :param x:
    :param y:
    :return:
    """
    # todo 判断图片的长宽度下限
    cur_pixel = img.getpixel((x, y))  # 当前像素点的值
    width = img.width
    height = img.height

    if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
        return 0

    if y == 0:  # 第一行
        if x == 0:  # 左上顶点,4邻域
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 4 - sum
        elif x == width - 1:  # 右上顶点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 4 - sum
        else:  # 最上非顶点,6邻域
            sum = img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - sum
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下顶点
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x, y - 1))
            return 4 - sum
        elif x == width - 1:  # 右下顶点
            sum = cur_pixel \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y - 1))

            return 4 - sum
        else:  # 最下非顶点,6邻域
            sum = cur_pixel \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x + 1, y - 1))
            return 6 - sum
    else:  # y不在边界
        if x == 0:  # 左边非顶点
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - sum
        elif x == width - 1:  # 右边非顶点
            # print('%s,%s' % (x, y))
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))
            return 6 - sum
        else:  # 具备9领域条件的
            sum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum


if __name__ == '__main__':
    file_path =r"F:\python_work\CINTEL_FZweb3_1_1\case\Prevent_situations\result\境外拦截top10.jpg"
    image = Image.open(file_path)        # 打开图像
    print(image.size)
    # image = fill_image(image)            # 将图像转为正方形，不够的地方补充为白色底色
    image_list = cut_image_operator(image,box=(566,365,1020,720))        # 分为图像
    save_images(image_list)              # 保存图像

    # 737,161
    #  737, 260
    # box=(600,161,737,260) operator
    # box=(566,418,1000,720)
    # 1200-180