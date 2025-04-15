#每次跑完，funasr会自动降级，不知道为什么。
# pip install -U funasr
import os
from datetime import datetime, timedelta
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
import librosa
import numpy as np
from pydub import AudioSegment
from pyannote.audio import Pipeline as SpeakerDiarizationPipeline

def diarize_audio(file_path, num_speakers=2, output_rttm="audio.rttm"):
    """
    使用pyannote/speaker-diarization-3.1模型对音频文件进行说话人分离

    参数:
        file_path (str): 输入的音频文件路径
        num_speakers (int): 预期的说话人数量，默认为2
        output_rttm (str): 输出的RTTM文件路径，默认为"audio.rttm"

    返回:
        None
    """
    speaker_diarization = SpeakerDiarizationPipeline.from_pretrained("pyannote/speaker-diarization-3.1")

    # 检查文件是否存在
    if not os.path.isfile(file_path):
        exit("File not found: {}".format(file_path))

    # 运行pipeline
    diarization = speaker_diarization(file_path, num_speakers=num_speakers)

    # 将结果写入RTTM文件
    with open(output_rttm, "w") as rttm:
        diarization.write_rttm(rttm)

    print("Done!")

#获取音频时长
def get_audio_duration(file_path):
    return  AudioSegment.from_wav(file_path).duration_seconds
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
# 定义提取音高的函数
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
# 定义提取响度的函数
def extract_loudness(file_path):
    """
    给定音频路径，提取并返回响度结果字典 loudness_result
    :param file_path: 音频文件路径
    :return: loudness_result 字典，包含时间点和对应的响度（dB）
    """
    y, sr = librosa.load(file_path, sr=22000)
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
# 加载情感模型
def load_emotion2vec():
    """
    加载预训练的模型。

    返回:
        model: 加载好的模型实例。
    """
    model_id = "iic/emotion2vec_plus_large"
    model = AutoModel(
        model=model_id,
        hub="ms",
        disable_update=True# "ms" 或 "modelscope" 针对中国大陆用户；"hf" 或 "huggingface" 针对海外用户
    )
    return model
# 加载语音识别模型
def load_sensevoice():
    model_dir = "iic/SenseVoiceSmall"

    model = AutoModel(
        model=model_dir,
        trust_remote_code=True,
        remote_code="./model.py",
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 30000},
        device="cuda:0",
        disable_update=True
    )
    return model
# 应用情感模型预测情感
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
# 应用语音识别模型识别文本
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

def calculate_speech_rate(text, duration):
    """
    计算语速，区分中英文
    
    参数:
        text: 识别出的文本
        duration: 音频时长（秒）
        
    返回:
        包含语速和语言的描述字符串
    """
    # 判断是否为中文
    if any('\u4e00' <= char <= '\u9fff' for char in text):
        # 中文：统计有效字符数
        chinese_chars = [char for char in text if '\u4e00' <= char <= '\u9fff']
        speech_rate = len(chinese_chars) / duration
        return f"His speech rate is {speech_rate:.2f} Chinese characters per second (Chinese)"
    else:
        # 英文：统计单词数
        speech_rate = len(text.split()) / duration
        return f"His speech rate is {speech_rate:.2f} words per second (English)"

def extract_audio_features(file_list:list,text_model,sar_model):
    """
    提取音频文件的特征信息，包括音高、响度、文本、语速和情感分析
    
    参数:
        file_list: 要处理的音频文件列表
        text_model: 语音识别模型
        sar_model: 情感分析模型
        
    返回:
        包含每个音频文件分析结果的字典
    """
    result = {}
    for file_path in file_list:
        file_name = os.path.basename(file_path)
        y, sr = librosa.load(file_path, sr=22000)
        # 提取音调音高
        f0, voiced_flag, voiced_probs = librosa.pyin(
            y, sr=sr,
            fmin=librosa.note_to_hz('C2'),
            fmax=librosa.note_to_hz('C7')
        )
        f0 = np.nan_to_num(f0, nan=-1.0)
        f0_list = f0.tolist()
        f0_list = [x for x in f0_list if x != -1.0]
        f0_mean = np.mean(f0_list)
        f0_std = np.std(f0_list)
        rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
        rms_db = librosa.amplitude_to_db(rms, ref=np.max)
        rms_list_db = rms_db.tolist()
        rms_list_db = [x for x in rms_list_db if x != 0]
        db_mean = np.mean(rms_list_db)
        db_std = np.std(rms_list_db)

        # 获取文本，语速
        text = get_text(file_path, text_model)
        duration = AudioSegment.from_wav(file_path).duration_seconds
        speech_rate_desc = calculate_speech_rate(text, duration)
        # 预测情绪
        emotion = predict_emotion(sar_model, file_path)
        # result.append(f"{file}:{len(text.split(' '))}  持续时间：{duration} 秒, 语速：{len(text.split(' ')) / duration} 词每秒\n {text}\nRMS平均值: {db_mean:.2f} dB \t RMS标准差: {db_std:.2f} dB\nF0平均值: {f0_mean:.2f} Hz \t F0标准差: {f0_std:.2f} Hz\n情感: {emotion}\n\n")
        describe_audio = f"From the audio analysis, the speaker said: {text}.\n{emotion}. \n {speech_rate_desc}, the average volume is {db_mean:.2f} dB \t the standard deviation of the volume is {db_std:.2f} dB. The average pitch is {f0_mean:.2f} Hz \t the standard deviation of the pitch is:{f0_std:.2f} Hz"
        result[file_name]=describe_audio


    return result



if __name__ == '__main__':
    file_list = os.listdir("../data/voice")
    text_model = load_sensevoice()
    sar_model = load_emotion2vec()
    result = extract_audio_features(file_list,text_model,sar_model)
    try:
        import json
        with open('outputs/results.json','w',encoding='utf-8') as f:
            json.dump(result,f,ensure_ascii=False,indent=4)
    except:
        with open('outputs/results.txt','w',encoding='utf-8') as f:
            for k,v in result.items():
                f.write(f"{k}:{v}\n")