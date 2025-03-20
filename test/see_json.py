import json
filename = "../src/outputs/output_results_2.json"


def parse_json_structure(data, parent=None):
    """
    递归解析JSON结构，替换值为默认占位符。
    :param data: JSON数据（字典或列表）
    :param parent: 用于递归的父节点
    :return: 解析后的JSON结构
    """
    if isinstance(data, dict):
        structure = {}
        for key, value in data.items():
            structure[key] = parse_json_structure(value, parent=key)
        return structure
    elif isinstance(data, list):
        if not data:
            return []
        # 如果列表中有多个元素，假设它们具有相同的结构
        element_structure = parse_json_structure(data[0])
        return [element_structure]
    else:
        # 如果是基本类型（str, int, float, bool, None）
        return f"{type(data)}"

def get_json_structure(file_path):
    """
    从文件路径中加载JSON，并解析其结构。
    :param file_path: JSON文件的路径
    :return: 解析后的JSON结构
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return parse_json_structure(json_data)
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except json.JSONDecodeError:
        print(f"无效的JSON文件: {file_path}")
    except Exception as e:
        print(f"发生错误: {e}")
    return None
structure = get_json_structure(filename)
if structure:
    print(json.dumps(structure, indent=2, ensure_ascii=False))