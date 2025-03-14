# pip install -U funasr
'''
Using the finetuned emotion recognization model

rec_result contains {'feats', 'labels', 'scores'}
	extract_embedding=False: 9-class emotions with scores
	extract_embedding=True: 9-class emotions with scores, along with features

9-class emotions:
iic/emotion2vec_plus_seed, iic/emotion2vec_plus_base, iic/emotion2vec_plus_large (May. 2024 release)
iic/emotion2vec_base_finetuned (Jan. 2024 release)
    0: angry
    1: disgusted
    2: fearful
    3: happy
    4: neutral
    5: other
    6: sad
    7: surprised
    8: unknown
'''

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
# wav_file = "../data/wav/test.wav"
wav_file = "../data/wav/output.wav"
# wav_file = f"{model.model_path}/example/test.wav"


rec_result = model.generate(wav_file, output_dir="./outputs", granularity="utterance", extract_embedding=False)
print(rec_result)

#找到字典中scorse最高对应的labels
max_score = max(rec_result[0]['scores'])
max_index = rec_result[0]['scores'].index(max_score)
max_label = rec_result[0]['labels'][max_index]
print(f"The most possible emotion is {max_label} with score {max_score}")