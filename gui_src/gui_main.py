import tkinter as tk
from http import HTTPStatus
from tkinter import font, messagebox
import cv2
from dashscope import Application
from tkinter import *
from PIL import Image, ImageTk
class ChatGUI:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("人机对话系统 2025-03-25")
        self.master.geometry("1000x600")

        self.custom_font = font.Font(family="Helvetica", size=12)
        self.cap =  cv2.VideoCapture(0)
        self.image_container =None
        self.is_recording = False
        self.video_writer = None
        self.video_canvas = None
        self.dialogue_log = []
        self.camera_img = None
        self.setup_main_layout()
        self.setup_chat_area()
        self.setup_video_area()
        self.setup_button_area()
        self.update_frame()



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
        # 设置背景颜色为白色
        video_frame = tk.Frame(self.right_frame, bg="white")
        video_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # 创建画布用于显示视频流
        image_width = 400
        image_height = 400
        self.video_canvas = Canvas(video_frame, bg='white', width=image_width, height=image_height)  # 绘制画布
        self.video_canvas.pack(fill=tk.BOTH, expand=True)

        # 添加文本标签说明这是一个视频区域
        # label = Label(video_frame, text='这是一个视频！', font=("黑体", 14), bg='white')
        # label.place(x=image_width / 2 - label.winfo_reqwidth() / 2, y=20)  # 使用place方法并尝试居中文本

        return video_frame

    def update_frame(self):
        # 读取一帧
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        if ret:
            # 将BGR格式转换为RGB格式
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 将帧转换为PIL图像
            im = Image.fromarray(frame)
            # 将PIL图像转换为Tkinter兼容的PhotoImage
            self.camera_img = ImageTk.PhotoImage(image=im)

            # # 更新Label的图像
            # self.video_canvas.config(image=img)
            self.video_canvas.create_image(0,0,anchor='nw',image=self.camera_img)  # 避免被垃圾回收

            # 每隔30ms更新一次帧
            self.master.after(30, self.update_frame)
        else:
            # 如果视频结束，释放资源
            self.cap.release()
            print("视频播放结束")

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

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter('output.avi', fourcc, 20.0, (int(self.cap.get(3)), int(self.cap.get(4))))
            self.update_video_feed()
            self.btn_start.config(text="正在录制...")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.cap.release()
            self.video_writer.release()
            self.video_label.config(text="视频采集区")
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
    app = ChatGUI()
    app.master.mainloop()



