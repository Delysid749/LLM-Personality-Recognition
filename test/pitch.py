import librosa
import numpy as np
file_path = r"../data/voice/1DCnIad1Y0w.002.wav"

y, sr = librosa.load(file_path, sr=22000)

# 提取基频
f0, voiced_flag, voiced_probs = librosa.pyin(
    y, sr=sr,
    fmin=librosa.note_to_hz('C2'),
    fmax=librosa.note_to_hz('C7')
)
f0 = np.nan_to_num(f0, nan=-1.0)

# 打印表头
print(f"音频文件: {file_path}")
print(f"采样率: {sr} Hz")
print("时间点(时:分:秒)\tF0值(Hz)\t音高名称")
f0_list = f0.tolist()
f0_list = [x for x in f0_list if x!= -1.0]
f0_mean = np.mean(f0_list)
f0_std = np.std(f0_list)
print(f"F0平均值: {f0_mean:.2f} Hz")
print(f"F0标准差: {f0_std:.2f} Hz")

