import librosa
import numpy as np
# audio_path =r"../data/voice/1DCnIad1Y0w.002.mp3"
audio_path =r"../data/voice/test_long.mp3"
# 加载音频
y, sr = librosa.load(audio_path, sr=None)

# 提取基频（F0）
f0, voiced_flag, voiced_probs = librosa.pyin(
    y, sr=sr, 
    fmin=librosa.note_to_hz('C2'),  # 最低频率（约65 Hz）
    fmax=librosa.note_to_hz('C7')   # 最高频率（约2093 Hz）
)

# 处理NaN值
f0 = np.nan_to_num(f0, nan=-1)

import matplotlib.pyplot as plt
plt.figure(figsize=(12, 4))
plt.plot(f0, label='F0')
plt.xlabel('Frame')
plt.ylabel('Frequency (Hz)')
plt.title('Pitch Contour')
plt.show()

def freq_to_note(freq):
    """将频率转换为音高名称"""
    if freq == 0:
        return "无声"
    
    # A4 = 440Hz 对应 MIDI 编号69
    semitone = 12 * np.log2(freq / 440.0) + 69
    semitone = int(round(semitone))
    
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (semitone - 12) // 12
    note = notes[semitone % 12]
    return f"{note}{octave}"

# 加载音频
file_path = "../data/voice/test_long.mp3"
y, sr = librosa.load(file_path, sr=None)

# 提取基频
f0, voiced_flag, voiced_probs = librosa.pyin(
    y, sr=sr,
    fmin=librosa.note_to_hz('C2'),
    fmax=librosa.note_to_hz('C7')
)
f0 = np.nan_to_num(f0, nan=0.0)

# 计算时间间隔参数
hop_length = 512  # librosa默认的帧移
frame_duration = hop_length / sr  # 每帧的持续时间（秒）

# 打印表头
print(f"音频文件: {file_path}")
print(f"采样率: {sr} Hz")
print("时间点(时:分:秒)\tF0值(Hz)\t音高名称")

# 遍历所有帧
for i in range(len(f0)):
    # 计算时间点
    total_seconds = i * frame_duration
    hours = int(total_seconds // 3600)
    remainder = total_seconds % 3600
    minutes = int(remainder // 60)
    seconds = remainder % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    
    # 格式化为时:分:秒.毫秒
    time_str = f"{hours:02d}:{minutes:02d}:{int(seconds):02d}.{milliseconds:03d}"
    
    # 获取音高名称
    current_f0 = f0[i]
    note_name = freq_to_note(current_f0) if current_f0 > 0 else "无声"
    
    # 输出结果
    print(f"{time_str}\t{current_f0:.2f}\t{note_name}")
