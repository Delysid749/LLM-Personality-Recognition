
import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk  # 图像控件

# 创建视频捕获对象，读取笔记本电脑的本地摄像头流
cap = cv2.VideoCapture(0)  # 使用本地摄像头，通常索引为0

# 界面画布更新图像
def tkImage():
    ref, frame = cap.read()
    if not ref:
        print("Failed to capture frame")
        return None
    frame = cv2.flip(frame, 1)  # 摄像头翻转
    cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    pilImage = Image.fromarray(cvimage)
    pilImage = pilImage.resize((4, image_height), Image.LANCZOS)
    tkImage = ImageTk.PhotoImage(image=pilImage)
    return tkImage

top = tk.Tk()
top.title('视频窗口')
top.geometry('900x600')
image_width = 600
image_height = 500
canvas = Canvas(top, bg='white', width=image_width, height=image_height)  # 绘制画布
Label(top, text='这是一个视频！', font=("黑体", 14), width=15, height=1).place(x=400, y=20, anchor='nw')
canvas.place(x=150, y=50)

# 保存图像对象，以防止被垃圾回收
image_container = None

def update_frame():
    global image_container
    pic = tkImage()
    if pic:
        canvas.create_image(0, 0, anchor='nw', image=pic)
        image_container = pic  # 保存引用
    else:
        print("No image to display")
    top.after(10, update_frame)  # 每10毫秒更新一次图像

top.after(10, update_frame)  # 启动定时器
top.mainloop()

# 释放摄像头
cap.release()
