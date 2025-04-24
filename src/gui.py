import tkinter as tk
from tkinter import filedialog, messagebox
from main import analyze_introduction_video
from audio_function import   load_sensevoice, load_emotion2vec
from predict import AIChatBot
class PersonalityAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("性格分析器")
        self.root.geometry("400x200")
        
        # 初始化模型
        self.text_model = load_sensevoice()
        self.sar_model = load_emotion2vec()
        self.chatbot = AIChatBot(model_path="../finetune/lora_model")
        
        # 创建界面元素
        self.create_widgets()
    
    def create_widgets(self):
        # 视频选择
        self.video_label = tk.Label(self.root, text="选择自我介绍视频:")
        self.video_label.pack(pady=10)
        
        self.video_entry = tk.Entry(self.root, width=40)
        self.video_entry.pack()
        
        self.browse_button = tk.Button(self.root, text="浏览", command=self.browse_video)
        self.browse_button.pack(pady=5)
        
        # 分析按钮
        self.analyze_button = tk.Button(self.root, text="开始分析", command=self.analyze_video)
        self.analyze_button.pack(pady=20)
        
        # 结果展示
        self.result_label = tk.Label(self.root, text="分析结果将显示在这里")
        self.result_label.pack()
    
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
        
        try:
            result = analyze_introduction_video(
                video_path=video_path,
                chatbot=self.chatbot,
                text_model=self.text_model,
                sar_model=self.sar_model
            )
            self.result_label.config(text=result)
            messagebox.showinfo("分析完成", "性格分析已完成！")
        except Exception as e:
            messagebox.showerror("错误", f"分析过程中出现错误:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalityAnalyzerApp(root)
    root.mainloop()