
from tqdm import tqdm
import json
import os
import sys
from pathlib import Path
current_file = Path(os.getcwd()).resolve()
project_root = current_file.parent
sys.path.append(str(project_root / 'src'))
from get_body_data import analyze_person_image
from audio_function import diarize_audio, extract_audio_features,load_sensevoice, load_emotion2vec, audio_dict2description
from video2voice import extract_audio
from preprocess_extract import merge_rttm_intervals, split_media_files,extract_middle_frame
text_model = load_sensevoice()
sar_model = load_emotion2vec()
print("模型加载完成")


def get_training_data(video_name):
    audio_dir = "../data/voice"
    video_dir = "../data/video"
    output_dir = "../data/output"  # 假设你有一个输出目录用于存放中间帧
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # 构建路径
    video_path = os.path.join(video_dir, video_name)
    audio_path = os.path.join(audio_dir, video_name.replace('.mp4', '.wav'))
    if not os.path.exists(audio_path):
        extract_audio(video_path, 'wav', audio_dir)
    frame_path = os.path.join(output_dir, video_name.replace('.mp4', '.jpg'))

    print(f"开始从视频 {video_path} 中提取音频...")
    # 提取音频特征
    print(f"正在分析 {audio_path} 的音频片段...")
    audio_features = extract_audio_features(audio_path, text_model, sar_model)
    audio_description = audio_dict2description(audio_features)

    # 提取视频中间帧并分析
    print(f"正在从视频 {video_path} 提取中间帧...")

    extract_middle_frame(video_path, frame_path)
    video_description = analyze_person_image(frame_path)

    # 组合描述
    combined_description = (
        f"Audio Analysis:\n{audio_description}\n\n"
        f"Video Analysis:\n{video_description}"
    )

    # 删除临时文件
    print("清理临时文件...")
    os.remove(frame_path)

    return combined_description


result = []
import json
import os
# 使用 tqdm 包装 os.listdir 的结果
video_files = os.listdir('../data/video')[300:]
for idx, i in enumerate(tqdm(video_files, desc="Processing videos")):
    if i.endswith('.mp4'):
        description = get_training_data(i)
        result.append({'video_name': i, 'description': description})
        os.system("cls")
        
        # 每处理100个文件保存一次
        if (idx + 1) % 100 == 0:
            if not os.path.exists('../data/output'):
                os.makedirs('../data/output')
            # 保存到新文件
            output_file = f'../data/output/result_{idx//100 + 1}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
            # 清空result以释放内存
            result = []


# 保存剩余的文件
if result:
    if not os.path.exists('../data/output'):
        os.makedirs('../data/output')
    output_file = f'../data/output/result_{len(video_files)//100 + 1}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

# 中断后继续运行的示例：
# 假设 result_8.json 已完好保存，说明已经处理了800个视频
# 修改 video_files 的切片范围，从第801个视频开始继续处理
# video_files = os.listdir('../data/video')[800:]  # 从第801个开始
# 然后重新运行代码即可