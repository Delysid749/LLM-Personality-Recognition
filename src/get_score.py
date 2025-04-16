import pandas as pd
import json
import os

# 读取pickle数据
data = pd.read_pickle('../data/annotation_training.pkl')

def get_big5_scores(data, video_name):
    result = {
        'videoName': video_name,
        "extraversion": None,
        "neuroticism": None,
        "agreeableness": None,
        "conscientiousness": None,
        "openness": None
    }

    for i in data["extraversion"].keys():
        if i == video_name:
            result['extraversion'] = round(data["extraversion"][i], 3)

    for i in data["neuroticism"].keys():
        if i == video_name:
            result['neuroticism'] = round(data["neuroticism"][i], 3)

    for i in data["agreeableness"].keys():
        if i == video_name:
            result['agreeableness'] = round(data["agreeableness"][i], 3)

    for i in data["conscientiousness"].keys():
        if i == video_name:
            result['conscientiousness'] = round(data["conscientiousness"][i], 3)

    for i in data["openness"].keys():
        if i == video_name:
            result['openness'] = round(data["openness"][i], 3)

    return result

def translate_big5_scores(big5_scores):
    return f"Their Big Five personality traits are:\nOpenness: {big5_scores['openness']}\nExtraversion: {big5_scores['extraversion']}\nNeuroticism: {big5_scores['neuroticism']}\nAgreeableness: {big5_scores['agreeableness']}\nConscientiousness: {big5_scores['conscientiousness']}"

if False:
    # 读取JSON文件
    with open('outputs/output_results.json', 'r', encoding='utf-8') as file:
        results = json.load(file)

    # 更新每个字典
    for entry in results:
        filename_without_extension = os.path.splitext(entry['filename'])[0]
        video_name = filename_without_extension + '.mp4'
        big5_score = get_big5_scores(data, video_name)
        entry['big5_score'] = big5_score

    # 写回JSON文件
    with open('outputs/output_results_2.json', 'w') as file:
        json.dump(results, file, indent=4)
#
if False:
    with open("../data/output/result.json", "r",encoding="utf-8") as f:
        results_data = json.load(f)
    result =[]
    for key in results_data.keys():
        filename_without_extension = os.path.splitext(key)[0]
        video_name = filename_without_extension + '.mp4'
        big5_score = get_big5_scores(data, video_name)
        temp = {
            "introduction":"What are his/her Big Five personality traits?",
            "input":results_data[key],
            "output":translate_big5_scores(big5_score)
        }
        result.append(temp)

    with open("../data/results.jsonl", "w", encoding="utf-8") as f:
        for i in result:
            print(i)
            f.write(json.dumps(i,ensure_ascii=False)+"\n")


with open("../data/output/result.json", "r",encoding="utf-8") as f:
        results_data = json.load(f)
result =[]
for i in results_data:
    filename = i["video_name"]
    big5_score = get_big5_scores(data, filename)
    temp = {
        "introduction":"What are his/her Big Five personality traits?",
        "input":i["description"],
        "output":translate_big5_scores(big5_score)
 
    }
    result.append(temp)

with open("../data/results.jsonl", "w", encoding="utf-8") as f:
    for i in result:
        print(i)
        f.write(json.dumps(i,ensure_ascii=False)+"\n")

