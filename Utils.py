from Constants import Constants
import os
import math

class Utils:
    def get_screen_shot(self, path):
        cmd = Constants.SCREENSHOT + path
        os.popen(cmd)

    def tap(self, position):
        cmd = Constants.TAP + str(position[0]) + " " + str(position[1])
        os.popen(cmd)

    def swipe(self, pos1, pos2, time):
        cmd = Constants.SWIPE + str(pos1[0]) + " " + str(pos1[1]) + " " + str(pos2[0]) \
              + " " + str(pos2[1]) + " " + str(time)
        os.popen(cmd)

    # 对比图片像素颜色值
    def comparePixelColor(self, srcImg, color, position, simThreshold):
        # 计算欧式空间距离
        # 首先获取 x 和 y 坐标的颜色值
        targetColor = self.getPixelColor(srcImg, position)
        # 再分别获取 R G B 值
        red = targetColor[0]
        green = targetColor[1]
        blue = targetColor[2]
        diff_red = red - color[0]
        diff_green = green - color[1]
        diff_blue = blue - color[2]
        similarity = (1 - math.sqrt(diff_red*diff_red + diff_blue*diff_blue + diff_green*diff_green) / math.sqrt(255*255 + 255*255 + 255*255))
        if similarity > simThreshold:
            return True
        else:
            return False

    # 获取图片坐标点颜色值
    def getPixelColor(self, srcImg, positon):
        srcImg = srcImg.convert('RGBA')
        str_strlist = srcImg.load()
        RGBA = str_strlist[positon[0], positon[1]]
        return RGBA