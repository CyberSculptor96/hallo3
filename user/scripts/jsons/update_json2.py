import os
import json

# 输入 JSON 文件路径
json_file_path = "/wangbenyou/huanghj/workspace/hallo3/examples/test_data-0320/fps24_121frames_in_label.json"

# 读取 JSON 数据
with open(json_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 处理每个条目
for item in data:
    for key, new_folder in [("video-path", "videos"), ("audio-path", "audios"), ("first-frame-path", "imgs")]:
        if key in item:
            original_path = item[key]
            parent_dir, filename = os.path.split(original_path)  # 拆分目录和文件名
            grandparent_dir = os.path.dirname(parent_dir)  # 获取上一级目录
            if new_folder == "audios":
                filename = filename.replace(".m4a", ".wav")
            new_path = os.path.join(grandparent_dir, new_folder, filename)  # 重新组合路径
            item[key] = new_path

# 保存修改后的 JSON 数据
output_json_path = json_file_path.replace(".json", "_updated.json")
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Updated JSON saved to: {output_json_path}")
