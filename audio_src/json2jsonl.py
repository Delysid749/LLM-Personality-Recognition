import json

# 读取JSON文件
with open('outputs/output_results_2.json', 'r') as file:
    results = json.load(file)

# 转换为JSONL格式
jsonl_data = []
for entry in results:
    instruction = "ta的五大性格为？"
    input_data = str({
        "emotion": entry["emotion"],
        "text": entry["text"],
        "basic_info": entry["basic_info"]
    })
    output_data = str(entry["big5_score"])

    jsonl_entry = {
        "instruction": instruction,
        "input": input_data,
        "output": output_data
    }
    jsonl_data.append(jsonl_entry)

# 写入JSONL文件
with open('outputs/output_results.jsonl', 'w', encoding='utf-8') as file:
    for entry in jsonl_data:
        file.write(json.dumps(entry) + '\n')



