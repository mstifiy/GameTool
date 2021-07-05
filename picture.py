# 基本思路：
# 1、屏幕抓取。
# 2、图片对比，找出不同之处。
# 3、找到不同之处的坐标值，利用win32api的mouse_event进行单击操作。
from ctypes import windll
import win32con
import win32gui
import numpy as np
from PIL import ImageGrab
import cv2 as cv
import time


def get_window_pos(name):
    # 获取窗口句柄
    handle = win32gui.FindWindow("#32770", name)
    if handle == 0:
        return None
    else:
        # DPI缩放级别对矩形有影响
        # Make program aware of DPI scaling
        user32 = windll.user32
        user32.SetProcessDPIAware()
        # 发送还原最小化窗口的信息
        win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        # 窗口高亮显示，防止被其他窗口覆盖
        win32gui.SetForegroundWindow(handle)
        time.sleep(0.5)

        return win32gui.GetWindowRect(handle), handle


def get_picture(wn):
    try:
        (x1, y1, x2, y2), handle = get_window_pos(wn)
    except TypeError:
        print(wn + "窗口不存在！")
    # print(x1, y1, x2, y2)

    # 截图
    img_ready = ImageGrab.grab((x1, y1, x2, y2))
    img_left = ImageGrab.grab((x1 + 134, y1 + 463, x1 + 134 + 582, y1 + 463 + 439))
    img_right = ImageGrab.grab((x1 + 820, y1 + 463, x1 + 820 + 582, y1 + 463 + 439))
    # 展示
    # img_ready.show()
    # img_left.show()
    # img_right.show()
    # 保存
    img_left.save("img1.jpg")
    img_right.save("img2.jpg")
    diff = cv.subtract(cv.cvtColor(np.asarray(img_left), cv.COLOR_BGR2RGB),
                       cv.cvtColor(np.asarray(img_right), cv.COLOR_BGR2RGB))
    # ret, dst = cv.threshold(diff, 20, 255, cv.THRESH_BINARY)
    # cv.imwrite("diff.jpg", diff)

    return diff


def processing(_img1, _img2):
    # 像素差异
    _diff = cv.subtract(_img1, _img2)

    # 轮廓差异
    gray1 = cv.cvtColor(_img1, cv.COLOR_BGR2GRAY)  # 转换成灰度图
    gray2 = cv.cvtColor(_img2, cv.COLOR_BGR2GRAY)

    # 二值化
    _, thresh1 = cv.threshold(gray1, 129, 255, cv.THRESH_BINARY)
    _, thresh2 = cv.threshold(gray2, 129, 255, cv.THRESH_BINARY)

    # 查找轮廓
    # binary-二值化结果，contours-轮廓信息，hierarchy-层级
    contours1, _ = cv.findContours(thresh1, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contours2, _ = cv.findContours(thresh2, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    # 显示轮廓，tmp为黑色的背景图
    tmp1 = np.zeros(_img1.shape, np.uint8)
    tmp2 = np.zeros(_img1.shape, np.uint8)
    res1 = cv.drawContours(tmp1, contours1, -1, (250, 255, 255), 1)
    res2 = cv.drawContours(tmp2, contours2, -1, (250, 255, 255), 1)

    _ContoursDiff = cv.subtract(res1, res2)
    cv.imshow('AllContours1', res1)
    cv.imshow('AllContours2', res2)

    return _diff
