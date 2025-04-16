import os
from pydub import AudioSegment
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip


def merge_rttm_intervals(file_path):
    """
    合并RTTM文件中同一说话人的连续时间区间
    
    参数:
        file_path: RTTM文件路径
        
    返回:
        包含合并后时间区间的列表，每个元素是一个字典，包含:
        - speaker: 说话人ID
        - start: 合并后的开始时间
        - end: 合并后的结束时间
    """
    merged_speakers = []
    previous_speaker_id = None
    current_start = None
    current_end = None

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 9:
                start = float(parts[3])
                duration = float(parts[4])
                speaker_id = parts[7]

                end = start + duration

                if speaker_id == previous_speaker_id:
                    # If the current speaker is the same as the previous one, extend the current interval
                    current_end = max(current_end, end)
                else:
                    # If the speaker has changed, finalize the previous interval and start a new one
                    if previous_speaker_id is not None:
                        merged_speakers.append(
                            {'speaker': previous_speaker_id, 'start': round(current_start,2), 'end': round(current_end,2)})

                    # Start a new interval
                    current_start = start
                    current_end = end
                    previous_speaker_id = speaker_id

        # Finalize the last interval after the loop ends
        if previous_speaker_id is not None:
            merged_speakers.append({'speaker': previous_speaker_id,'start': round(current_start,2), 'end': round(current_end,2)})

    return merged_speakers


def split_media_files(merged_speakers, video_file_path, output_dir):
    # 加载视频文件
    video = VideoFileClip(video_file_path)
    
    # 从视频中提取音频
    audio = video.audio
    audio_file_path = os.path.splitext(video_file_path)[0] + ".wav"
    audio.write_audiofile(audio_file_path)
    
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取第一个说话人的ID
    if merged_speakers:
        first_speaker = merged_speakers[0]['speaker']
        
        # 创建说话人子目录
        speaker_dir = os.path.join(output_dir, first_speaker)
        if not os.path.exists(speaker_dir):
            os.makedirs(speaker_dir)
        
        # 处理第一个说话人的所有片段
        for interval in merged_speakers:
            if interval['speaker'] == first_speaker:
                start = interval['start']
                end = interval['end']
                
                # 分割视频
                video_segment = video.subclipped(start, end)
                video_filename = f"{first_speaker}_{start}_{end}.mp4"
                video_output_path = os.path.join(speaker_dir, video_filename)
                video_segment.write_videofile(video_output_path, codec="libx264")
                
                # 分割音频
                audio_segment = audio.subclipped(start, end)
                audio_filename = f"{first_speaker}_{start}_{end}.wav"
                audio_output_path = os.path.join(speaker_dir, audio_filename)
                audio_segment.write_audiofile(audio_output_path)
    
    video.close()


def extract_middle_frame(video_file_path, output_path):
    """
    从视频中截取中间一帧并保存为图片
    
    参数:
        video_file_path: 视频文件路径
        output_path: 输出图片路径
    """
    video = VideoFileClip(video_file_path)
    duration = video.duration
    middle_time = duration / 2
    frame = video.get_frame(middle_time)
    
    # 使用moviepy的ImageClip保存帧
    ImageSequenceClip([frame], fps=1).save_frame(output_path)
    video.close()


if __name__ == '__main__':
    # Example usage
    file_path = '../data/ai_test_2.rttm'
    video_file_path = '../data/ai_test_2.mp4'  # 改为视频文件路径
    output_dir = 'outputs'  # 输出目录
    
    if not os.path.exists(file_path):
        print('File not found:', file_path)
        exit()
    
    # 获取合并后的说话人区间
    result = merge_rttm_intervals(file_path)
    
    # 打印结果
    for item in result:
        print(item)
    
    # # 分割媒体文件
    # if os.path.exists(video_file_path):
    #     split_media_files(result, video_file_path, output_dir)
    #     print(f"媒体分割完成，结果保存在 {output_dir} 目录")
    # else:
    #     print('视频文件未找到:', video_file_path)



