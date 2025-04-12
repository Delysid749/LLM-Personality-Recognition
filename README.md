# LLM-Personality-Recognition

requirements.txt

ffmpeg software

# 如果运行我们的项目来进行数据的预处理，请安装根目录下的requirements.txt文件中的依赖包。
# 如果运行我们的模型调优方法，请再建一个环境，然后安装finetune 下的requirements.txt文件中的依赖包。

目前项目中test,book_try是测试文件，但是随着主代码的更新，这些测试文件已经不能再保证运行了（就是没用了，但是又不想删)


# 使用到了pyannotespeaker
需要保存share token,命令为huggingface-cli login

# 音频处理模块说明

本模块主要用于从视频中提取音频，并进行说话人分离和音频特征分析。

## 主要功能

1. **音频提取**
   - 从视频文件中提取音频，支持多种视频格式（mp4, avi, mov, mkv, flv, wmv）
   - 使用FFmpeg进行音频提取，输出格式为wav

2. **说话人分离**
   - 使用pyannote/speaker-diarization-3.1模型进行说话人分离
   - 生成RTTM格式的说话人分离结果文件

3. **音频特征分析**
   - 提取音频的以下特征：
     - 音高（Pitch）
     - 响度（Loudness）
     - 语速（Speech Rate）
     - 情感分析（Emotion）
   - 使用SenseVoice模型进行语音识别
   - 使用Emotion2Vec模型进行情感分析

4. **结果输出**
   - 将分析结果保存为JSON格式
   - 每个说话人的分析结果包括：
     - 语音文本
     - 情感分析结果
     - 音高和响度随时间变化的数据
     - 语速信息

## 依赖项

- FFmpeg
- PyTorch
- Librosa
- Pyannote.audio
- FunASR
- Modelscope

## 使用说明

1. 安装依赖：
   ```bash
   pip install -r requirements.txt