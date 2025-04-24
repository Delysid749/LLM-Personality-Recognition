# LLM-Personality-Recognition

## 项目简介

欢迎来到 **LLM-Personality-Recognition**！本项目致力于通过多种方法提取视频中的特征信息，并将其转化为文本，最终构建一个可调优且不依赖多模态功能的大语言模型（LLM）。我们利用先进的特征提取技术和自然语言生成方法，将视频中的视觉、音频等多模态信息转化为高质量的文本描述，为大语言模型的训练提供丰富的数据支持。此外，我们还引入了 **unsloth** 工具对 LLM 进行调优，以进一步提升模型的性能和泛化能力。

## 项目目标

1. **特征提取**：从视频中提取关键的视觉和音频特征，包括人物的面部表情、肢体语言、语音语调等。
2. **特征转文本**：将提取到的特征信息转化为自然语言描述，生成详细的文本内容。
3. **大语言模型训练**：利用生成的文本数据训练大语言模型，使其能够理解和生成与视频内容相关的人格特质描述。
4. **模型调优**：通过 **unsloth** 工具对 LLM 进行调优，提升模型的性能，使其在特定任务上表现出色。



# 安装

如果运行我们的项目来进行数据的预处理，请安装根目录下的requirements.txt文件中的依赖包。

## 使用到了pyannotespeaker

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
   ```

# data目录中数据来源说明

本项目中的数据均来源于 **First Impressions V2 (CVPR'17)** 数据集。如果您在研究或项目中使用了这些数据，请务必引用 **First Impressions V2 (CVPR'17)** 数据集的相关文献，以及本项目的说明。数据集的具体信息如下：

- **数据集名称**：First Impressions V2

- **数据集来源**：[https://chalearnlap.cvc.uab.cat/dataset/24/description/](https://chalearnlap.cvc.uab.cat/dataset/24/description/)

- **数据集描述**：包含 10,000 个视频片段，平均时长为 15 秒，涵盖不同性别、年龄、国籍和种族的人物。视频标注基于五大人格特质（Extraversion、Agreeableness、Conscientiousness、Neuroticism 和 Openness），并扩展了新的语言数据（转录文本）和新的面试标注（job-interview variable）。

- **引用要求**：请引用以下文献：

  ```
  @inproceedings{escalante2017first,
    title={First Impressions V2: A Large-Scale Dataset for Apparent Personality Analysis},
    author={Escalante, H. Jair and Escalera, Sergio and Guyon, Isabelle},
    booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
    year={2017}
  }
  ```



### 引用

本项目基于以下开源项目，模型，api：

1. **FunASR**
   - 项目地址：[https://github.com/modelscope/FunASR](https://github.com/modelscope/FunASR)
   - 项目简介：FunASR 是一个基础的端到端语音识别工具包，提供了开源的 SOTA 预训练模型，支持语音识别、语音活动检测、文本后处理等功能。
   - 引用文献：
     ```
     @inproceedings{gao2023funasr,
       author={Zhifu Gao and Zerui Li and Jiaming Wang and Haoneng Luo and Xian Shi and Mengzhe Chen and Yabin Li and Lingyun Zuo and Zhihao Du and Zhangyu Xiao and Shiliang Zhang},
       title={FunASR: A Fundamental End-to-End Speech Recognition Toolkit},
       year={2023},
       booktitle={INTERSPEECH},
     }
     @inproceedings{An2023bat,
       author={Keyu An and Xian Shi and Shiliang Zhang},
       title={BAT: Boundary aware transducer for memory-efficient and low-latency ASR},
       year={2023},
       booktitle={INTERSPEECH},
     }
     @inproceedings{gao22b_interspeech,
       author={Zhifu Gao and ShiLiang Zhang and Ian McLoughlin and Zhijie Yan},
       title={Paraformer: Fast and Accurate Parallel Transformer for Non-autoregressive End-to-End Speech Recognition},
       year=2022,
       booktitle={Proc. Interspeech 2022},
       pages={2063--2067},
       doi={10.21437/Interspeech.2022-9996}
     }
     @inproceedings{shi2023seaco,
       author={Xian Shi and Yexin Yang and Zerui Li and Yanni Chen and Zhifu Gao and Shiliang Zhang},
       title={SeACo-Paraformer: A Non-Autoregressive ASR System with Flexible and Effective Hotword Customization Ability},
       year={2023},
       booktitle={ICASSP2024}
     }
     ```
以下是针对你提到的四个项目的中文引用部分：


2. **pyannote.audio**
**项目名称**：pyannote.audio  
**项目简介**：pyannote.audio 是一个用于说话人日志（Speaker Diarization）的开源工具包，基于 PyTorch 框架，提供了最先进的预训练模型和流程，可以进一步针对自己的数据进行微调以提升性能。  
**引用文献**：
```
@inproceedings{Plaquet23,
  author={Alexis Plaquet and Hervé Bredin},
  title={{Powerset multi-class cross entropy loss for neural speaker diarization}},
  year=2023,
  booktitle={Proc. INTERSPEECH 2023},
}
```

3. **SenseVoice**
**项目名称**：SenseVoice  
**项目地址**：[https://github.com/FunAudioLLM/SenseVoice](https://github.com/FunAudioLLM/SenseVoice)  
**项目简介**：SenseVoice 是一个多语言语音理解基础模型，支持多种语音理解能力，包括自动语音识别（ASR）、语言识别（LID）、语音情感识别（SER）和音频事件检测（AED）。  
**引用文献**：
```
@inproceedings{gao2023funasr,
  author={Zhifu Gao and Zerui Li and Jiaming Wang and Haoneng Luo and Xian Shi and Mengzhe Chen and Yabin Li and Lingyun Zuo and Zhihao Du and Zhangyu Xiao and Shiliang Zhang},
  title={FunASR: A Fundamental End-to-End Speech Recognition Toolkit},
  year={2023},
  booktitle={INTERSPEECH},
}
```

4. **emotion2vec/emotion2vec_plus_large**
**模型名称**：emotion2vec+  
**模型简介**：emotion2vec+ 是一系列用于语音情感识别（SER）的基础模型，旨在通过数据驱动的方法克服语言和录音环境的影响，实现通用且鲁棒的情感识别能力。其性能显著优于 Hugging Face 上其他高下载量的开源模型。  
**引用文献**：
```
@article{ma2023emotion2vec,
  title={emotion2vec: Self-Supervised Pre-Training for Speech Emotion Representation},
  author={Ma, Ziyang and Zheng, Zhisheng and Ye, Jiaxin and Li, Jinchao and Gao, Zhifu and Zhang, Shiliang and Chen, Xie},
  journal={arXiv preprint arXiv:2312.15185},
  year={2023}
}
```
5. **unsloth**
   **模型名称：**unsloth  
   **模型简介：**unsloth 是一个用于优化和微调大型语言模型（LLM）的工具，能够显著提升模型的性能和泛化能力。它通过高效的优化策略和灵活的微调机制，帮助用户快速调整模型以适应特定任务需求，从而实现更好的模型表现。unsloth 支持多种主流的 LLM 框架，并提供了易于使用的接口，方便用户集成到现有的模型训练和优化流程中。
   **引用链接：**
     [unsloth GitHub 仓库](https://github.com/unslothai/unsloth)
     https://github.com/unslothai/unsloth
   **引用文献：**
```
    @software{unsloth,
      author = {Daniel Han, Michael Han and Unsloth team},
      title = {Unsloth},
      url = {http://github.com/unslothai/unsloth},
      year = {2023}
    }
```
6. **阿里云人体结构化属性 API**
   **模型名称：**阿里云人体结构化属性 API  
   **模型简介：**阿里云视觉智能开放平台提供的 人体结构化属性 API 是一个强大的工具，用于检测图片中人体的属性，包括性别、年龄、朝向、帽子、眼镜、包、衣服颜色等。该 API 提供了丰富的人体属性检测功能，能够为视频分析和特征提取提供重要的支持。通过高效的检测算法和优化的接口设计，该 API 能够快速、准确地返回人体属性的分析结果，适用于多种应用场景，如智能安防、视频监控、行为分析等。
   **引用链接：**
      [阿里云视觉智能开放平台 - 人体结构化属性 API](https://help.aliyun.com/zh/viapi/developer-reference/api-human-body-structuralization-attribute)
      https://help.aliyun.com/zh/viapi/developer-reference/api-human-body-structuralization-attribute

   
   



### 数据集引用

本项目使用了 **First Impressions V2 (CVPR'17)** 数据集，该数据集由 ChaLearn 提供，包含从 YouTube 高清视频中提取的 10,000 个视频片段，平均时长为 15 秒。数据集分为训练集、验证集和测试集，比例为 3:1:1。视频中的人物具有不同的性别、年龄、国籍和种族。数据集的标注基于五大人格特质（Extraversion、Agreeableness、Conscientiousness、Neuroticism 和 Openness），通过 Amazon Mechanical Turk (AMT) 生成，确保了标注的可靠性。此外，数据集还扩展了新的语言数据（转录文本）和新的面试标注（job-interview variable），以补充现有的感官数据（视频）和人格特质标注。

引用文献：

```
@inproceedings{escalante2017first,
  title={First Impressions V2: A Large-Scale Dataset for Apparent Personality Analysis},
  author={Escalante, H. Jair and Escalera, Sergio and Guyon, Isabelle},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2017}
}
```



### 免责声明

1. 本项目基于上述开源项目和模型进行开发，其核心功能和部分代码依赖于这些开源资源。我们对原项目的作者和贡献者表示衷心的感谢。
2. 本项目在使用上述开源项目和模型时，严格遵守其开源协议和许可证（如 MIT License 等）。如果您发现本项目存在任何违反开源协议的行为，请及时联系我们，我们将立即进行整改。
3. 本项目仅供学习和研究使用，未经授权，不得用于商业用途。如果您需要将本项目用于商业用途，请务必与相关开源项目的版权所有者联系，获取适当的授权。
4. 本项目的开发和使用不保证完全无误，我们不对因使用本项目而产生的任何直接或间接损失承担责任。用户在使用本项目时，应自行评估其风险，并确保其符合自身需求和法律法规的要求。

