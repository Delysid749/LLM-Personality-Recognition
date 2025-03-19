import librosa
import os
file_list = os.listdir("../data/voice/")

if False:
    # 加载音频文件
    def get_speech_rate(audio_path):
        y, sr = librosa.load(audio_path, sr=None)

        # 计算总时长
        duration = len(y) / sr

        # 分割音频，找出语音片段
        segments = librosa.effects.split(y, top_db=30)

        # 统计语音片段的数量作为总音节数
        syllable_count = len(segments)

        # 计算语速
        speech_rate = syllable_count / duration
        # print(f"语速（Speech Rate）：{speech_rate} 音节每秒")
        return f"语速（Speech Rate）：{speech_rate} 音节每秒"

    # file_path = "../data/voice/1DCnIad1Y0w.002.wav"
    # print(get_speech_rate(file_path))

    for file in file_list[0:10]:
        file_path = "../data/voice/" + file
        print(f"{file}:{get_speech_rate(file_path)}")
        # print(get_speech_rate(file_path))

from audio_function import load_sensevoice,get_text
model = load_sensevoice()
for file in file_list[0:10]:
    file_path = "../data/voice/" + file
    text = get_text(file_path,model)