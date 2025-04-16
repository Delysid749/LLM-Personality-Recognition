import os
from audio_function import diarize_audio, extract_audio_features,load_sensevoice, load_emotion2vec, audio_dict2description
from video2voice import extract_audio
from get_body_data import analyze_person_image
from preprocess_extract import merge_rttm_intervals, split_media_files,extract_middle_frame
import json
from predict import AIChatBot




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

    # # 进行说话人分离
    print("开始进行说话人分离...")
    rttm_path = os.path.join(output_dir, "audio.rttm")
    diarize_audio(audio_path, output_rttm=rttm_path)
    print(f"说话人分离完成，结果已保存到: {rttm_path}")



    # 合并说话人区间
    print("正在合并说话人区间...")
    merged_intervals = merge_rttm_intervals(rttm_path)
    
    # 分割音频
    print("开始分割音频,视频...")
    split_media_files(merged_intervals, video_path, output_dir)
    print("音频,视频分割完成")

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

    if os.path.exists(speaker_dir):
        audio_files = [f for f in os.listdir(speaker_dir) if f.endswith('.wav')]
        audio_files = [os.path.join(speaker_dir, f) for f in audio_files]
        
        # 提取音频特征
        print(f"正在分析说话人 {speaker} 的音频片段...")
        features = {}
        for audio_file in audio_files:
            file_name = os.path.basename(audio_file)
            # 处理音频文件
            audio_features = extract_audio_features(audio_file, text_model, sar_model)
            audio_description = audio_dict2description(audio_features)
            video_file = os.path.join(speaker_dir, file_name.replace('.wav', '.mp4'))
            if os.path.exists(video_file):
                frame_file = os.path.join(speaker_dir, file_name.replace('.wav', '.jpg'))
                extract_middle_frame(video_file, frame_file)
                video_description = analyze_person_image(frame_file)
                combined_description = f"Audio Analysis:\n{audio_description}\n\nVideo Analysis:\n{video_description}"
            else:
                combined_description = f"Audio Analysis:\n{audio_description}\n\nVideo Analysis: No video file found"
            
            features[file_name] = combined_description
        print("所有音频片段处理完成")
    else:
        print(f"说话人目录 {speaker_dir} 不存在")

    # 保存结果
    result_path = os.path.join(output_dir, "results.json")
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(features, f, ensure_ascii=False, indent=4)

    print(f"处理完成，结果保存在 {result_path}")
    return features
    




def predict_personality(features, chatbot):
    """
    根据分析结果预测性格
    :param features: process_video函数返回的特征字典
    :param chatbot: 已初始化的AIChatBot实例
    :return: 性格预测结果
    """
    # 构建提示词
    prompt = """
    # Role
    You are a professional psychologist specializing in assessing personality traits through analyzing individuals' behaviors and speech. Your task is to provide a detailed personality analysis based on the information provided by the user, and give specific scores from 0-1 for the Big Five personality traits.

    - **Task**: Based on the information provided by the user (such as behavior descriptions, speech expressions, etc.), evaluate the individual's Big Five personality traits and provide specific scores from 0-1.
    - **Openness**: Assess the individual's curiosity, imagination, and acceptance of new things.
    - **Conscientiousness**: Assess the individual's sense of responsibility, organizational skills, and self-discipline.
    - **Extraversion**: Assess the individual's sociability, energy, and optimism.
    - **Agreeableness**: Assess the individual's cooperativeness, empathy, and trustworthiness.
    - **Neuroticism**: Assess the individual's emotional stability, anxiety levels, and stress coping abilities.

    ## Constraints
    - Evaluate based solely on the information provided by the user, ensuring the assessment is objective and accurate.
    - Even if the information provided by the user may be incomplete, You will still try your best to give the scores for the Big Five personality traits.

    ### Input:
    {analysis}
    ### Response:
    """
    
    results = {}
    for file_name, analysis in features.items():
        full_prompt = prompt.format(analysis=analysis)
        prediction = chatbot.generate_response(full_prompt)
        results[file_name] = prediction
    
    result_path = os.path.join("outputs", "personality_predictions.json")
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print(f"性格预测完成，结果保存在 {result_path}")
    return results

# 在main函数中使用示例
if __name__ == "__main__":
    video_path = "../data/ai_test_2.mp4"  # 替换为你的视频路径
    # features = process_video(video_path)
    with open('outputs/results.json', 'r', encoding='utf-8') as f:
        features = json.load(f)
    
    # 初始化chatbot
    chatbot = AIChatBot(model_path="../finetune/lora_model")
    
    # 进行性格预测
    personality_results = predict_personality(features, chatbot)
    print("性格预测结果：")
    for  prediction in personality_results.values():
        print(prediction)