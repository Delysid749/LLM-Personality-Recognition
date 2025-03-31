import tkinter as tk
from tkinter import font, messagebox
import cv2
from threading import Thread
import time
from dashscope import Application
import os
from http import HTTPStatus
from PIL import Image, ImageTk

class ChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("人机对话系统 2025-03-25")
        master.geometry("1000x600")

        self.custom_font = font.Font(family="Helvetica", size=12)

        self.setup_main_layout()
        self.setup_chat_area()
        self.setup_video_area()
        self.setup_button_area()

        self.cap = cv2.VideoCapture(0)  # 使用本地摄像头，通常索引为0
        self.is_recording = False
        self.video_writer = None
        self.dialogue_log = []

        self.image_width = 400
        self.image_height = 400

        # 自动启动摄像头预览
        self.start_camera_preview()

    def setup_main_layout(self):
        """创建主容器分区"""
        # 左右分栏布局
        self.left_frame = tk.Frame(self.master, bg="#90EE90")  # 浅绿色
        self.right_frame = tk.Frame(self.master, bg="#E0FFFF")  # 浅青色

        # 使用Grid布局管理器
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # 配置网格权重
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=2)
        self.master.grid_rowconfigure(0, weight=1)

    def setup_chat_area(self):
        """配置左侧聊天区域"""
        # AI标识
        self.canvas = tk.Canvas(self.left_frame, width=60, height=60,
                                bg="#90EE90", highlightthickness=0)
        self.canvas.create_oval(10, 10, 50, 50, fill="#800080")  # 紫色圆形
        self.canvas.create_text(30, 30, text="AI", fill="#FFC0CB",
                                font=("Arial", 16, "bold"))

        # 对话内容显示
        self.chat_text = tk.Text(self.left_frame, width=40, height=20,
                                 bg="#90EE90", fg="#FF69B4",  # 粉红色
                                 font=self.custom_font, wrap=tk.WORD)
        self.chat_text.tag_configure("separator", foreground="black", spacing3=1)

        # 插入示例对话
        self.chat_text.insert(tk.END, "AI: Hello, what can I do for you.")
        self.chat_text.insert(tk.END, "\n――――――――――――――\n", "separator")
        self.chat_text.insert(tk.END, "User: what is Apple?")
        self.chat_text.insert(tk.END, "\n――――――――――――――\n", "separator")
        self.chat_text.config(state=tk.DISABLED)  # 设为只读

        # 布局管理
        self.canvas.pack(side=tk.LEFT, padx=10)
        self.chat_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def setup_video_area(self):
        """配置右侧视频采集区"""
        video_frame = tk.Frame(self.right_frame, bg="white")
        video_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # 视频占位符
        self.video_label = tk.Label(video_frame,
                                    bg="#E0FFFF", fg="red",
                                    font=("Arial", 24, "bold"),
                                    width=20, height=10)
        self.video_label.pack(expand=True)

        # 创建画布
        self.canvas = tk.Canvas(video_frame, bg='white', width=self.image_width, height=self.image_height)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # 保持正方形
        video_frame.pack_propagate(False)
        video_frame.config(width=400, height=400)

    def setup_button_area(self):
        """配置底部按钮区"""
        button_frame = tk.Frame(self.right_frame, bg="#808080")  # 灰色背景
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # 按钮样式
        btn_style = {
            "bg": "#FFFF00",  # 黄色
            "fg": "red",
            "activebackground": "#CCCC00",
            "font": ("Arial", 12, "bold"),
            "width": 10,
            "height": 2
        }

        # 创建三个按钮
        self.btn_start = tk.Button(button_frame, text="开始", **btn_style, command=self.start_recording)
        self.btn_stop = tk.Button(button_frame, text="结束", **btn_style, command=self.stop_recording)
        self.btn_hold = tk.Button(button_frame, text="保留", **btn_style, command=self.save_dialogue_and_video)

        # 按钮布局
        self.btn_start.pack(side=tk.LEFT, padx=20, pady=10)
        self.btn_stop.pack(side=tk.LEFT, padx=20)
        self.btn_hold.pack(side=tk.LEFT, padx=20)

    def start_camera_preview(self):
        self.update_video_feed()

    def update_video_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)  # 摄像头翻转
            frame_resized = cv2.resize(frame, (self.image_width, self.image_height))
            cvimage = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGBA)
            pilImage = Image.fromarray(cvimage)
            tkImage = ImageTk.PhotoImage(image=pilImage)
            self.video_label.config(image="")
            self.canvas.create_image(0, 0, anchor='nw', image=tkImage)
            self.canvas.image = tkImage  # 保存对 PhotoImage 的引用
        self.master.after(30, self.update_video_feed)

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter('output.avi', fourcc, 20.0, (self.image_width, self.image_height))
            self.btn_start.config(text="正在录制...")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.video_writer.release()
            self.btn_start.config(text="开始")

    def save_dialogue_and_video(self):
        with open("dialogue.txt", "w") as f:
            f.write("\n".join(self.dialogue_log))
        messagebox.showinfo("保存成功", "对话内容和视频已保存")

    def send_message_to_ai(self, message):
        api_key = "sk-8ac1a297ccc9487cafcf22a43bc8c4b8"
        response = Application.call(
            api_key=api_key,
            app_id='YOUR_APP_ID',  # 替换为实际的应用 ID
            prompt=message
        )

        if response.status_code != HTTPStatus.OK:
            print(f'request_id={response.request_id}')
            print(f'code={response.status_code}')
            print(f'message={response.message}')
            print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
        else:
            ai_response = response.output.text
            self.dialogue_log.append(f"User: {message}")
            self.dialogue_log.append(f"AI: {ai_response}")
            self.display_message(message, "User")
            self.display_message(ai_response, "AI")

    def display_message(self, message, sender):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"{sender}: {message}\n")
        self.chat_text.insert(tk.END, "――――――――――――――\n", "separator")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatGUI(root)
    root.mainloop()
    # 释放摄像头
    app.cap.release()



