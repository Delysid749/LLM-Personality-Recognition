import os
from audio_function import diarize_audio, extract_audio_features,load_sensevoice, load_emotion2vec, audio_dict2description
from video2voice import extract_audio
from get_body_data import analyze_person_image
from preprocess_extract import merge_rttm_intervals, split_media_files,extract_middle_frame
import json
from predict import AIChatBot
import shutil
import re



def analyse_dialogue_first(video_path,text_model,sar_model, output_dir="outputs"):
    """
    分析视频对话的主要处理函数
    1. 从视频中提取音频
    2. 进行说话人分离
    3. 合并说话人区间并分割音视频
    4. 对第一个说话人的音频片段进行特征提取和分析
    5. 结合视频分析生成综合描述
    6. 保存分析结果
    注意，运行程序后会生成一个名为output_dir所指向的目录，用于保存所有输出文件，注意手动清除缓存。
    
    :param video_path: 输入视频文件路径
    :param output_dir: 输出目录，默认为"outputs"
    :return: 包含所有分析结果的特征字典
    """
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
                combined_description = f"{audio_description}\n\nVideo Analysis:\n{video_description}"
            else:
                combined_description = f"{audio_description}\n\nVideo Analysis: No video file found"
            
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

def clear_cache(output_dir="outputs"):
    """
    清除指定目录下的所有缓存文件
    :param output_dir: 要清除的目录，默认为"outputs"
    """
    if os.path.exists(output_dir):
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))
        print(f"已清除缓存目录: {output_dir}")
    else:
        print(f"缓存目录 {output_dir} 不存在")


def analyze_introduction_video(video_path, chatbot,text_model,sar_model, output_dir="outputs"):
    """
    分析自我介绍视频并预测性格
    :param video_path: 自我介绍视频路径
    :param chatbot: 已初始化的AIChatBot实例
    :param output_dir: 输出目录，默认为"outputs"
    :return: AI输出的性格预测结果
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已创建输出目录: {output_dir}")
    # 从视频中提取音频
    print("正在提取音频...")
    video_filename = os.path.basename(video_path)
    audio_filename = os.path.splitext(video_filename)[0] + ".wav"
    audio_path = os.path.join(output_dir, audio_filename)
    extract_audio(video_path, voice_dir=output_dir)
    print(f"音频已成功提取并保存到: {audio_path}")
    # 提取音频特征并生成描述
    print("正在分析音频...")
    audio_features = extract_audio_features(audio_path, text_model, sar_model)
    audio_description = audio_dict2description(audio_features)
    # 提取视频中间帧并分析
    print("正在分析视频...")
    frame_path = os.path.join(output_dir, "middle_frame.jpg")
    extract_middle_frame(video_path, frame_path)
    video_description = analyze_person_image(frame_path)
    # 合并描述
    combined_description = f"{audio_description}\n\nVideo Analysis:\n{video_description}"
    # 进行性格预测
    print("正在进行性格预测...")
    features = {"introduction": combined_description}
    personality_result = predict_personality(features, chatbot)
    try:
        big5_score = chatbot.get_scores_from_text(personality_result["introduction"])
        print(personality_result["introduction"])
        return big5_score
    except:
        return personality_result["introduction"]


def main_dialogue_first(video_path,chatbot,text_model,sar_model, output_dir="outputs"):
    clear_cache()
    features = analyse_dialogue_first(video_path, text_model,sar_model, output_dir)
    # 提取duration的正则表达式
    duration_pattern = r"Audio Duration: (\d+\.\d+) seconds"
    # 提取speech_rate的正则表达式
    speech_rate_pattern = r"Speech rate is (\d+\.\d+) (?:Chinese characters|words) per second"
    # 计算每个片段的文本量
    text_volumes = {}
    for file_name, description in features.items():
        # 提取duration
        duration_match = re.search(duration_pattern, description)
        duration = float(duration_match.group(1)) if duration_match else 0
        
        # 提取speech_rate
        rate_match = re.search(speech_rate_pattern, description)
        speech_rate = float(rate_match.group(1)) if rate_match else 0
        
        # 计算文本量
        text_volumes[file_name] = duration * speech_rate
    # 进行性格预测
    personality_results = predict_personality(features, chatbot)

    traits_dicts = {}
    for file_name, result in personality_results.items():
        traits_dicts[file_name] = chatbot.get_scores_from_text(result)
    total_text_volume = sum(text_volumes.values())
    weighted_scores = {
        'Openness': 0,
        'Conscientiousness': 0,
        'Extraversion': 0,
        'Agreeableness': 0,
        'Neuroticism': 0
    }

    # 计算加权分数
    for file_name in text_volumes.keys():
        weight = text_volumes[file_name] / total_text_volume
        print(f"片段 {file_name} 的权重为 {weight:.2f}, 性格预测结果为 {traits_dicts[file_name]}")
        for trait, score in traits_dicts[file_name].items():
            weighted_scores[trait] += score * weight
    for trait in weighted_scores.keys():
        weighted_scores[trait] = round(weighted_scores[trait], 3)
    print("\n" + "-" * 50)
    print("性格预测结果：")
    print(weighted_scores)
    print("-" * 50)
    return weighted_scores

def demo_1(video_path = "..\\data\\video\\0G9vplL8ae8.001.mp4" ):
    clear_cache()
    print("正在加载模型...")
    text_model = load_sensevoice()
    sar_model = load_emotion2vec()
    chatbot = AIChatBot(model_path="../finetune/lora_model")
    result = main_dialogue_first(video_path, chatbot,text_model,sar_model)
    print("\n"*5+"-"*50)
    print("性格预测结果：")
    print(result)
    print("-"*50)

def demo_2(video_path = "..\\data\\video\\0G9vplL8ae8.001.mp4" ):
    clear_cache()
    print("正在加载模型...")
    text_model = load_sensevoice()
    sar_model = load_emotion2vec()
    chatbot = AIChatBot(model_path="../finetune/lora_model")
    result = analyze_introduction_video(video_path, chatbot,text_model,sar_model)
    print("\n"*5+"-"*50)
    print("性格预测结果：")
    print(result)
    print("-"*50)
# 在main函数中使用示例
if __name__ == "__main__":
    demo_2()


