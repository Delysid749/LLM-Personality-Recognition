from unsloth import FastLanguageModel
import torch
import json

class AIChatBot:
    def __init__(self, model_path, max_seq_length=2048, dtype=None, load_in_4bit=True):
        """
        初始化AI聊天机器人
        :param model_path: 模型路径
        :param max_seq_length: 最大序列长度，默认2048
        :param dtype: 数据类型，None表示自动检测
        :param load_in_4bit: 是否使用4bit量化，默认True
        """
        self.max_seq_length = max_seq_length
        self.dtype = dtype
        self.load_in_4bit = load_in_4bit
        
        # 加载模型
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name = model_path,
            max_seq_length = max_seq_length,
            dtype = dtype,
            load_in_4bit = load_in_4bit,
        )
        
    def generate_response(self, message, max_new_tokens=512, temperature=0.7, top_p=0.9):
        """
        生成AI回复
        :param message: 输入消息
        :param max_new_tokens: 最大生成token数，默认512
        :param temperature: 温度参数，默认0.7
        :param top_p: top-p采样参数，默认0.9
        :return: AI生成的回复
        """
        inputs = self.tokenizer(
            [message], 
            return_tensors = "pt"
        ).to("cuda")
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens = max_new_tokens,
            temperature = temperature,
            top_p = top_p,
        )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# 示例用法
if __name__ == "__main__":
    # 初始化聊天机器人
    chatbot = AIChatBot(model_path="../finetune/lora_model")
    
    # 获取用户输入并生成回复
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = chatbot.generate_response(user_input)
        print(f"AI: {response}")