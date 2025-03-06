import os
import subprocess

def extract_audio_from_video(video_dir, voice_dir, output_format="mp3"):
    # 确保输出目录存在
    if not os.path.exists(voice_dir):
        os.makedirs(voice_dir)

    # 遍历视频目录中的所有文件
    for filename in os.listdir(video_dir):
        if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')):
            video_path = os.path.join(video_dir, filename)
            audio_filename = os.path.splitext(filename)[0] + f".{output_format}"
            audio_path = os.path.join(voice_dir, audio_filename)

            # 使用 ffmpeg 提取音频
            command = f'ffmpeg -i "{video_path}" -vn -c:a libmp3lame -q:a 2 "{audio_path}"'
            subprocess.run(command, shell=True)

if __name__ == "__main__":
    # 假设 video 和 voice 目录与脚本同级
    current_dir = os.getcwd()
    video_dir = os.path.join(current_dir, "../data/video")
    voice_dir = os.path.join(current_dir, "../data/voice")

    extract_audio_from_video(video_dir, voice_dir)