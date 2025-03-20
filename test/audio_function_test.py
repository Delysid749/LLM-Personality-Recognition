import librosa
import numpy as np
import os
from pydub import AudioSegment
from src.audio_function import load_sensevoice,get_text,load_emotion2vec,predict_emotion
file_list = os.listdir("../data/voice/")
text_model = load_sensevoice()
sar_model =  load_emotion2vec()
result = []
for file in file_list[0:2]:
    file_path = "../data/voice/" + file
    y, sr = librosa.load(file_path, sr=22000)

    # 提取音调音高
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y, sr=sr,
        fmin=librosa.note_to_hz('C2'),
        fmax=librosa.note_to_hz('C7')
    )
    f0 = np.nan_to_num(f0, nan=-1.0)
    print(f"音频文件: {file_path}", end="\t")
    print(f"采样率: {sr} Hz")
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

    #获取文本，语速
    text = get_text(file_path, text_model)
    duration = AudioSegment.from_wav(file_path).duration_seconds
    # 预测情绪
    emotion = predict_emotion(sar_model,file_path )
    result.append(f"{file}:{len(text.split(' '))}  持续时间：{duration} 秒, 语速：{len(text.split(' '))/duration} 词每秒\n {text}\nRMS平均值: {db_mean:.2f} dB \t RMS标准差: {db_std:.2f} dB\nF0平均值: {f0_mean:.2f} Hz \t F0标准差: {f0_std:.2f} Hz\n情感: {emotion}\n\n")


for i in result:
    print(i)
