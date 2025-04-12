import os
from audio_function import diarize_audio, extract_audio_features
from video2voice import extract_audio
from audio_function import load_sensevoice, load_emotion2vec

def process_video(video_path, output_dir="outputs"):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 从视频中提取音频
    audio_path = os.path.join(output_dir, "extracted_audio.wav")
    extract_audio(video_path, voice_dir=output_dir)

    # 进行说话人分离
    rttm_path = os.path.join(output_dir, "audio.rttm")
    diarize_audio(audio_path, output_rttm=rttm_path)

    # 加载模型
    text_model = load_sensevoice()
    sar_model = load_emotion2vec()

    # 处理每个说话人的音频片段
    results = {}
    with open(rttm_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 9:
                speaker = parts[7]
                start = float(parts[3])
                end = start + float(parts[4])

                # 分割音频
                output_file = os.path.join(output_dir, f"{speaker}_{start}_{end}.wav")
                command = f'ffmpeg -i "{audio_path}" -ss {start} -to {end} -c copy "{output_file}"'
                os.system(command)

                # 提取音频特征
                features = extract_audio_features([output_file], text_model, sar_model)
                results[speaker] = features

    # 保存结果
    result_path = os.path.join(output_dir, "results.json")
    with open(result_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"处理完成，结果保存在 {result_path}")

if __name__ == "__main__":
    video_path = "../data/ai_test_2.mp4"  # 替换为你的视频路径
    process_video(video_path)