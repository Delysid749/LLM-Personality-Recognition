
from funasr import AutoModel

# model="iic/emotion2vec_base"
# model="iic/emotion2vec_base_finetuned"
# model="iic/emotion2vec_plus_seed"
# model="iic/emotion2vec_plus_base"
model_id = "iic/emotion2vec_plus_large"

model = AutoModel(
    model=model_id,
    hub="ms",  # "ms" or "modelscope" for China mainland users; "hf" or "huggingface" for other overseas users
)
wav_file = "../data/voice/1DCnIad1Y0w.002.wav"

rec_result = model.generate(wav_file, output_dir="../src/outputs", granularity="utterance", extract_embedding=False)
print(rec_result)

#找到字典中scorse最高对应的labels
max_score = max(rec_result[0]['scores'])
max_index = rec_result[0]['scores'].index(max_score)
max_label = rec_result[0]['labels'][max_index]
print(f"The most possible emotion is {max_label} with score {max_score}")