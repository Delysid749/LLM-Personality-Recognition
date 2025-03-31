import tkinter as tk
from tkinter import font


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
        # AI标识 [[62]][[70]]
        self.canvas = tk.Canvas(self.left_frame, width=60, height=60,
                                bg="#90EE90", highlightthickness=0)
        self.canvas.create_oval(10, 10, 50, 50, fill="#800080")  # 紫色圆形
        self.canvas.create_text(30, 30, text="AI", fill="#FFC0CB",
                                font=("Arial", 16, "bold"))

        # 对话内容显示 [[124]][[63]]
        self.chat_text = tk.Text(self.left_frame, width=40, height=20,
                                 bg="#90EE90", fg="#FF69B4",  # 粉红色
                                 font=self.custom_font, wrap=tk.WORD)
        self.chat_text.tag_configure("separator", foreground="black", spacing3=1)

        # 插入示例对话 [[用户需求]]
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

        # 视频占位符 [[172]][[174]]
        self.video_label = tk.Label(video_frame,
                                    text="视频采集区",
                                    bg="#E0FFFF", fg="red",
                                    font=("Arial", 24, "bold"),
                                    width=20, height=10)
        self.video_label.pack(expand=True)

        # 保持正方形 [[用户需求]]
        video_frame.pack_propagate(False)
        video_frame.config(width=400, height=400)

    def setup_button_area(self):
        """配置底部按钮区"""
        button_frame = tk.Frame(self.right_frame, bg="#808080")  # 灰色背景
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # 按钮样式 [[177]][[178]]
        btn_style = {
            "bg": "#FFFF00",  # 黄色
            "fg": "red",
            "activebackground": "#CCCC00",
            "font": ("Arial", 12, "bold"),
            "width": 10,
            "height": 2
        }

        # 创建三个按钮 [[用户需求]]
        self.btn_start = tk.Button(button_frame, text="开始", **btn_style)
        self.btn_stop = tk.Button(button_frame, text="结束", **btn_style)
        self.btn_hold = tk.Button(button_frame, text="保留", **btn_style)

        # 按钮布局
        self.btn_start.pack(side=tk.LEFT, padx=20, pady=10)
        self.btn_stop.pack(side=tk.LEFT, padx=20)
        self.btn_hold.pack(side=tk.LEFT, padx=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatGUI(root)
    root.mainloop()
