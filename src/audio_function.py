#每次跑完，funasr会自动降级，不知道为什么。
# pip install -U funasr
import librosa
import numpy as np
from datetime import datetime, timedelta
from funasr import AutoModel
import os
import json
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess


# 解析时间字符串为秒
def parse_time_to_seconds(time_str):
    t = datetime.strptime(time_str, "%M:%S.%f")
    delta = timedelta(minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
    return delta.total_seconds()


# 将秒数格式化为时间字符串
def format_seconds_to_time(seconds):
    td = timedelta(seconds=seconds)
    time_str = str(td)[2:-3] if len(str(td)) > 7 else f"0{str(td)[:-3]}"
    return time_str


# 读取文件内容到字典
def read_file_to_dict(file_path, delimiter='\t'):
    result = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            key, value = line.strip().split(delimiter)
            result[key] = float(value) if delimiter == '\t' else value
    return result


# 定义将频率转换为音高名称的函数
def freq_to_note(freq):
    """将频率转换为音高名称"""
    if freq == 0 or freq == -1.0:  # 增加对-1.0的判断，对应np.nan转换的结果
        return "unknown"

    semitone = 12 * np.log2(freq / 440.0) + 69
    semitone = int(round(semitone))
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (semitone - 12) // 12
    note = notes[semitone % 12]
    return f"{note}{octave}"


def extract_pitch(file_path):
    """
    给定音频路径，提取并返回pitch_result字典
    :param file_path: 音频文件路径
    :return: pitch_result 字典
    """
    y, sr = librosa.load(file_path, sr=22000)
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y, sr=sr,
        fmin=librosa.note_to_hz('C2'),
        fmax=librosa.note_to_hz('C7')
    )
    f0 = np.nan_to_num(f0, nan=-1.0)

    hop_length = 512
    times = librosa.frames_to_time(np.arange(len(f0)), sr=sr, hop_length=hop_length)

    result = {}
    for i in range(len(f0)):
        time_seconds = times[i]
        minutes = int(time_seconds // 60)
        seconds = int(time_seconds % 60)
        milliseconds = int((time_seconds - int(time_seconds)) * 1000)
        time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        current_f0 = f0[i]
        note_name = freq_to_note(current_f0)
        result[time_str] = [round(current_f0, 2), note_name]

    pitch_result = {}
    reserve_value = None
    last_key = None
    for key, value in sorted(result.items()):
        if last_key is None or reserve_value != value[1]:
            pitch_result[key] = value[1]
            reserve_value = value[1]
        last_key = key

    return pitch_result



def extract_loudness(file_path):
    """
    给定音频路径，提取并返回响度结果字典 loudness_result
    :param file_path: 音频文件路径
    :return: loudness_result 字典，包含时间点和对应的响度（dB）
    """
    # 加载音频文件
    y, sr = librosa.load(file_path, sr=22000)

    # 计算短时RMS能量
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]

    # 转换为分贝（dB）
    rms_db = librosa.amplitude_to_db(rms, ref=np.max)

    # 计算时间轴（秒）
    times = librosa.frames_to_time(np.arange(len(rms_db)), sr=sr, hop_length=512)

    loudness_result = {}
    # 打印带有时分秒和对应音量的信息，并填充loudness_result字典
    for time_seconds, db in zip(times, rms_db):
        minutes = int(time_seconds // 60)
        seconds = int(time_seconds % 60)
        milliseconds = int((time_seconds - int(time_seconds)) * 1000)
        # 格式化为时:分:秒.毫秒
        time_str = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        loudness_result[time_str] = round(db, 2)  # 保留两位小数

    return loudness_result


# 合并字典
def merge_dicts(pitch_result, loudness_result):
    merged_result = {}

    # 将时间转换为秒以便比较
    pitch_times_seconds = {parse_time_to_seconds(k): v for k, v in pitch_result.items()}
    loudness_times_seconds = {parse_time_to_seconds(k): v for k, v in loudness_result.items()}
    # loudness_times_seconds = {parse_time_to_seconds(k.split(': ')[0]): float(k.split(': ')[1]) for k in loudness_result}
    # 找到最近的时间点进行对齐
    for pitch_time_s, pitch_value in pitch_times_seconds.items():
        closest_loudness_time_s = min(loudness_times_seconds.keys(), key=lambda x: abs(x - pitch_time_s))
        closest_loudness_value = loudness_times_seconds[closest_loudness_time_s]

        # 格式化时间回字符串形式
        pitch_time_str = format_seconds_to_time(pitch_time_s)
        merged_result[pitch_time_str] = {
            'Pitch': pitch_value,
            'Loudness': "{:.2f}".format(closest_loudness_value)
            # 'Loudness': closest_loudness_value
        }

    return merged_result
# 输出合并后的结果


def load_emotion2vec():
    """
    加载预训练的模型。

    返回:
        model: 加载好的模型实例。
    """
    model_id = "iic/emotion2vec_plus_large"
    model = AutoModel(
        model=model_id,
        hub="ms",  # "ms" 或 "modelscope" 针对中国大陆用户；"hf" 或 "huggingface" 针对海外用户
    )
    return model

def load_sensevoice():
    model_dir = "iic/SenseVoiceSmall"

    model = AutoModel(
        model=model_dir,
        trust_remote_code=True,
        remote_code="./model.py",
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 30000},
        device="cuda:0",
    )
    return model

def predict_emotion(model, wav_file):
    """
    使用给定的模型预测音频文件的情感。

    参数:
        model: 已加载的模型实例。
        wav_file: 要分析的音频文件路径。

    返回:
        formatted_result: 格式化后的情感结果字符串。
    """
    rec_result = model.generate(wav_file, output_dir="./outputs", granularity="utterance", extract_embedding=False)

    if not rec_result or not rec_result[0].get('scores') or not rec_result[0].get('labels'):
        return "无法识别情感"

    max_score = max(rec_result[0]['scores'])
    max_index = rec_result[0]['scores'].index(max_score)
    max_label = rec_result[0]['labels'][max_index]

    formatted_result = f"The most possible emotion is {max_label} with score {max_score}"
    return formatted_result


def get_text(wav_file,model):
    res = model.generate(
        input=wav_file,
        cache={},
        language="auto",  # "zh", "en", "yue", "ja", "ko", "nospeech"
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,  #
        merge_length_s=15,
    )
    text = rich_transcription_postprocess(res[0]["text"])
    # print(text)
    return text

def process_wav_files(directory):
    """
    批量处理目录中的所有 .wav 文件

    参数:
        directory: 包含 .wav 文件的目录路径。
    """
    funasr_model = load_emotion2vec()
    sensevoice_model = load_sensevoice()
    results = []

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.wav'):
                wav_file = os.path.join(root, file_name)
                text_result = get_text(wav_file, sensevoice_model)
                emo_result = predict_emotion(funasr_model, wav_file)
                loudness_result = extract_loudness(wav_file)
                pitch_result = extract_pitch(wav_file)
                merged_result = merge_dicts(pitch_result, loudness_result)

                result_dict = {
                    "filename": os.path.basename(wav_file),
                    "emotion": emo_result,
                    "text":text_result,
                    "basic_info": merged_result
                }

                results.append(result_dict)
    return results





if __name__ == "__main__":
    input_directory = r"../data/voice"  # 替换为你的输入目录
    output_json = r"./output_results.json"  # 替换为你想要保存的JSON文件路径

    results=process_wav_files(input_directory)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

"""
# 示例调用
if __name__ == "__main__":
    model = load_model()
    wav_file = r"../data/voice/1DCnIad1Y0w.002.wav"
    emo_result = predict_emotion(model, wav_file)
    loudness_result = extract_loudness(wav_file)
    pitch_result = extract_pitch(wav_file)
    merged_result = merge_dicts(pitch_result, loudness_result)
    for key, value in merged_result.items():
        print(f"{key}\t Pitch: {value['Pitch']}\t Loudness: {value['Loudness']}")
    print(emo_result)
    result_dict = {
        "filename": os.path.basename(wav_file),
        "merged_result": merged_result,
        "emotion": emo_result
    }
"""