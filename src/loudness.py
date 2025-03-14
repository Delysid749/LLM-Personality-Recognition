import librosa
import numpy as np

# 加载音频文件
audio_path = r"../data/voice/1DCnIad1Y0w.002.mp3"
y, sr = librosa.load(audio_path, sr=22000)

# 计算短时RMS能量
rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]

# 转换为分贝（dB）
rms_db = librosa.amplitude_to_db(rms, ref=np.max)

# 计算时间轴（秒）
times = librosa.frames_to_time(np.arange(len(rms_db)), sr=sr, hop_length=512)


print(times)
loudness_result = {}
# # 打印带有时分秒和对应音量的信息
for time_seconds, db in zip(times, rms_db):
    minutes = int(time_seconds // 60)
    seconds = int(time_seconds % 60)
    milliseconds = int((time_seconds - int(time_seconds)) * 1000)
    # 格式化为时:分:秒.毫秒
    time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    print(f"{time_str}, Volume (dB): {db:.2f}")
    loudness_result[time_str] = db


with open('loudness_result.txt', 'w') as f:
    for key, value in loudness_result.items():
        f.write(f"{key}: {value}\n")