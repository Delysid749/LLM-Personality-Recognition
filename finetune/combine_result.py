import os
import json
from pathlib import Path

def combine_results(output_dir="../data/output"):
    # 获取所有result文件
    result_files = sorted(
        [f for f in os.listdir(output_dir) if f.startswith('result_') and f.endswith('.json')],
        key=lambda x: int(x.split('_')[1].split('.')[0])
    )
    
    combined_result = []
    
    # 逐个读取并合并
    for result_file in result_files:
        with open(os.path.join(output_dir, result_file), 'r', encoding='utf-8') as f:
            data = json.load(f)
            combined_result.extend(data)
    
    # 保存合并后的结果
    output_path = os.path.join(output_dir, 'combined_result.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(combined_result, f, ensure_ascii=False, indent=4)
    
    print(f"合并完成，结果保存在 {output_path}")

if __name__ == "__main__":
    combine_results()