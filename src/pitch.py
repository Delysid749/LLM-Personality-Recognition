import librosa
import numpy as np

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
# file_path = "../data/voice/test.mp3"
file_path = r"../data/voice/1DCnIad1Y0w.002.mp3"

y, sr = librosa.load(file_path, sr=22000)

# 提取基频
f0, voiced_flag, voiced_probs = librosa.pyin(
    y, sr=sr,
    fmin=librosa.note_to_hz('C2'),
    fmax=librosa.note_to_hz('C7')
)
f0 = np.nan_to_num(f0, nan=-1.0)

# 计算时间间隔参数
hop_length = 512  # 帧移
times = librosa.frames_to_time(np.arange(len(f0)), sr=sr, hop_length=hop_length)

# 打印表头
print(f"音频文件: {file_path}")
print(f"采样率: {sr} Hz")
print("时间点(时:分:秒)\tF0值(Hz)\t音高名称")

result = {}
# 遍历所有帧
for i in range(len(f0)):
    time_seconds = times[i]
    minutes = int(time_seconds // 60)
    seconds = int(time_seconds % 60)
    milliseconds = int((time_seconds - int(time_seconds)) * 1000)
    # 格式化为时:分:秒.毫秒
    time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    current_f0 = f0[i]
    note_name = freq_to_note(current_f0) if current_f0 > 0 else "无声"
    result[time_str] = [round(current_f0, 2), note_name]

pitch_result = {}
reserve_time = next(iter(result))
reserve_value = result[reserve_time][1]
pitch_result[reserve_time] = reserve_value


for key in result.keys():
    if reserve_value != result[key][1]:
        pitch_result[key] = result[key][1]
        reserve_value = result[key][1]

for key in pitch_result.keys():
    # print(key, new_result[key]
    print(f"{key}\t{pitch_result[key]}")


# with open('pitch_result.txt', 'w', encoding='utf-8') as f:
#     for key,value in pitch_result.items():
#         f.write(f"{key}\t{value}\n")
