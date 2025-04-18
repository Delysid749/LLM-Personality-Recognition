import os
import subprocess
import time
def extract_audio_from_videos(video_dir, voice_dir, output_format="wav"):
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
            command = f'ffmpeg -i "{video_path}"  -ac 1 "{audio_path}"'
            subprocess.run(command, shell=True)
            # time.sleep(1) # 等待 ffmpeg 完成


def extract_audio(file_path: str, output_format: str = 'wav', voice_dir: str = './'):
    if os.path.isfile(file_path):
        filename = os.path.basename(file_path)
        audio_filename = os.path.splitext(filename)[0] + f".{output_format}"
        audio_path = os.path.join(voice_dir, audio_filename)

        # 确保输出目录存在
        if not os.path.exists(voice_dir):
            os.makedirs(voice_dir)

        # 使用 ffmpeg 提取音频，-y 参数覆盖已存在文件
        command = f'ffmpeg -y -i "{file_path}" -ac 1 -ar 16000 -vn "{audio_path}"'
        subprocess.run(command, shell=True)


if __name__ == "__main__":
    # 假设 video 和 voice 目录与脚本同级
    # current_dir = os.getcwd()
    # video_dir = os.path.join(current_dir, "../data/video")
    # voice_dir = os.path.join(current_dir, "../data/voice")
    #
    # extract_audio_from_videos(video_dir, voice_dir)
    file_path = '../data/ai_test_2.mp4'
    extract_audio(file_path,)