import os
from audio_function import diarize_audio, extract_audio_features
from video2voice import extract_audio
from audio_function import load_sensevoice, load_emotion2vec





def process_video(video_path, output_dir="outputs"):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已创建输出目录: {output_dir}")

    # 从视频中提取音频
    print(f"开始从视频 {video_path} 中提取音频...")
    video_filename = os.path.basename(video_path)
    audio_filename = os.path.splitext(video_filename)[0] + ".wav"
    audio_path = os.path.join(output_dir, audio_filename)
    extract_audio(video_path, voice_dir=output_dir)
    print(f"音频已成功提取并保存到: {audio_path}")

    # 进行说话人分离
    print("开始进行说话人分离...")
    rttm_path = os.path.join(output_dir, "audio.rttm")
    diarize_audio(audio_path, output_rttm=rttm_path)
    print(f"说话人分离完成，结果已保存到: {rttm_path}")



    # 合并说话人区间
    print("正在合并说话人区间...")
    from preprocess_extract import merge_rttm_intervals, split_media_files
    merged_intervals = merge_rttm_intervals(rttm_path)
    
    # 分割音频
    print("开始分割音频...")
    split_media_files(merged_intervals, video_path, output_dir)
    print("音频分割完成")

    # 处理每个说话人的音频片段
    print("开始处理每个说话人的音频片段...")
    speaker = merged_intervals[0]['speaker']  
    speaker_dir = os.path.join(output_dir, speaker)

    # 加载模型
    print("正在加载语音识别和情感分析模型...")
    text_model = load_sensevoice()
    sar_model = load_emotion2vec()
    print("模型加载完成")
    
    # 开启双线程，一个线程处理音频，一个线程处理视频

    # 音频处理线程
    if os.path.exists(speaker_dir):
        audio_files = [f for f in os.listdir(speaker_dir) if f.endswith('.wav')]
        audio_files = [os.path.join(speaker_dir, f) for f in audio_files]
        
        # 提取音频特征
        print(f"正在分析说话人 {speaker} 的音频片段...")
        features = extract_audio_features(audio_files, text_model, sar_model)
        print("所有音频片段处理完成")
    else:
        print(f"说话人目录 {speaker_dir} 不存在")

    # 保存结果
    result_path = os.path.join(output_dir, "results.json")
    with open(result_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(features, f, ensure_ascii=False, indent=4)

    print(f"处理完成，结果保存在 {result_path}")

if __name__ == "__main__":
    video_path = "../data/ai_test_2.mp4"  # 替换为你的视频路径
    process_video(video_path)