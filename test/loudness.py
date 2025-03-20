import librosa
import numpy as np

# 加载音频文件
audio_path = r"../data/voice/1DCnIad1Y0w.002.wav"
y, sr = librosa.load(audio_path, sr=22000)

# 计算短时RMS能量
rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]

# 转换为分贝（dB）
rms_db = librosa.amplitude_to_db(rms, ref=np.max)

rms_list_db =rms_db.tolist()
rms_list_db = [x for x in rms_list_db if x!= 0]
db_mean = np.mean(rms_list_db)
db_std = np.std(rms_list_db)
print(f"RMS平均值: {db_mean:.2f} dB")
print(f"RMS标准差: {db_std:.2f} dB")


