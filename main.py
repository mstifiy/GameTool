import wx
from wx.adv import Animation, AnimationCtrl
from picture import get_picture
import gif


class Frame(wx.Frame):
    def __init__(self):
        no_resize = wx.DEFAULT_FRAME_STYLE & ~ wx.RESIZE_BORDER
        wx.Frame.__init__(self, None, -1, title = 'MSTIFIY', pos = (0, 0), size = (600, 1000), style = no_resize)
        self.panel = wx.Panel(self, -1)
        self.button = wx.Button(self.panel, -1, "开始运行", (0, 445))
        self.button.Size = wx.Size(100, 50)
        self.button.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.run, self.button)
        self.animation = AnimationCtrl(self.panel)

    def run(self, evt):
        windowName = "大家来找茬"
        dst = get_picture(windowName)
        # cv.imshow("dst", dst)
        gif.create_gif(["img1.jpg", "img2.jpg"], "diff.gif", 0.1)
        self.animation.Stop()
        self.animation = AnimationCtrl(self.panel, -1, Animation('diff.gif'), pos = (0, 0))  # 创建一个动画
        self.animation.Play()  # 播放动图


        row, col, x = dst.shape
        bmp = wx.Bitmap.FromBuffer(col, row, dst)
        wx.StaticBitmap(self, -1, bmp, (0, 500), (bmp.GetWidth(), bmp.GetHeight()))  # BUG:静态图更新延迟


if __name__ == '__main__':
    app = wx.App()
    Frame().Show()
    app.MainLoop()
