import tkinter as tk
from tkinter import filedialog, messagebox
from main import analyze_introduction_video, main_dialogue_first
from audio_function import load_sensevoice, load_emotion2vec
from predict import AIChatBot

class PersonalityAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("性格分析器")
        self.root.geometry("600x400")
        
        # 初始化模型
        self.text_model = load_sensevoice()
        self.sar_model = load_emotion2vec()
        self.chatbot = AIChatBot(model_path="../finetune/lora_model")
        
        # 视频类型标志
        self.is_intro_video = True
        
        # 创建界面元素
        self.create_widgets()
    
    def create_widgets(self):
        # 视频选择
        self.video_label = tk.Label(self.root, text="选择视频:")
        self.video_label.pack(pady=10)
        
        self.video_entry = tk.Entry(self.root, width=40)
        self.video_entry.pack()
        
        self.browse_button = tk.Button(self.root, text="浏览", command=self.browse_video)
        self.browse_button.pack(pady=5)
        
        # 视频类型切换按钮
        self.video_type_button = tk.Button(
            self.root, 
            text="当前类型: 自述视频",
            command=self.toggle_video_type
        )
        self.video_type_button.pack(pady=5)
        
        # 分析按钮
        self.analyze_button = tk.Button(self.root, text="开始分析", command=self.analyze_video)
        self.analyze_button.pack(pady=20)
        
        # 结果展示
        self.result_label = tk.Label(self.root, text="分析结果将显示在这里")
        self.result_label.pack()
    
    def toggle_video_type(self):
        self.is_intro_video = not self.is_intro_video
        text = "自述视频" if self.is_intro_video else "对话视频"
        self.video_type_button.config(text=f"当前类型: {text}")
    
    def browse_video(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("视频文件", "*.mp4")]
        )
        if file_path:
            self.video_entry.delete(0, tk.END)
            self.video_entry.insert(0, file_path)
    
    def analyze_video(self):
        video_path = self.video_entry.get()
        if not video_path:
            messagebox.showwarning("警告", "请先选择一个mp4格式的视频文件")
            return
        
        # 清除之前的结果
        self.result_label.config(text="分析中...")
        
        try:
            if self.is_intro_video:
                result = analyze_introduction_video(
                    video_path=video_path,
                    chatbot=self.chatbot,
                    text_model=self.text_model,
                    sar_model=self.sar_model
                )
            else:
                result = main_dialogue_first(
                    video_path=video_path,
                    chatbot=self.chatbot,
                    text_model=self.text_model,
                    sar_model=self.sar_model
                )
            
            if type(result) == dict:
                result_text = "".join([f"{k}: {v:.2f}\n" for k, v in result.items()])
                self.result_label.config(text=result_text)
            else:
                self.result_label.config(text=result)
        except Exception as e:
            self.result_label.config(text="分析结果将显示在这里")
            messagebox.showerror("错误", f"分析过程中出现错误:\n{str(e)}")

if __name__ == "__main__":
    print("loading....")
    root = tk.Tk()
    app = PersonalityAnalyzerApp(root)
    root.mainloop()