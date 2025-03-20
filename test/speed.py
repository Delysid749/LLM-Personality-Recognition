import librosa
import os


file_list = os.listdir("../data/voice/")
from pydub import AudioSegment


from src.audio_function import load_sensevoice,get_text
model = load_sensevoice()
result = []
for file in file_list[0:10]:
    file_path = r"../data/voice/" + file
    text = get_text(file_path,model)
    duration = AudioSegment.from_wav(file_path).duration_seconds
    result.append(f"{file}:{len(text.split(' '))}  持续时间：{duration} 秒, 语速：{len(text.split(' '))/duration} 词每秒\n {text}\n")
for i in result:
    print(i)


