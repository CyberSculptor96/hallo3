import os
import json

# 加载现有的 JSON 文件
input_json_path = '/wangbenyou/huanghj/workspace/hallo3/json/data_sampled_filtered.json'
output_json_path = '/wangbenyou/huanghj/workspace/hallo3/json/data_sampled_filtered_updated.json'

# 读取现有的 JSON 文件
with open(input_json_path, 'r') as f:
    data = json.load(f)

# 获取 output_testset 文件夹路径
output_testset_path = '/wangbenyou/huanghj/workspace/hallo3/output/output_testset'

# 更新视频路径
for item in data:
    from pathlib import Path
    video_file_name = Path(item['video-path']).stem
    
    # 查找对应的文件夹
    matching_folder = None
    for folder in os.listdir(output_testset_path):
        if video_file_name in folder:
            matching_folder = folder
            break
    
    # 如果找到了匹配的文件夹，获取其 "seedxxx" 部分
    if matching_folder:
        seed_part = matching_folder.split('-')[-1]  # 获取 seedxxx 部分
        new_video_path = item['video-path'].replace(video_file_name, f"{video_file_name}-{seed_part}")
        item['video-path'] = new_video_path  # 更新 video-path

# 将更新后的数据保存为新的 JSON 文件
with open(output_json_path, 'w') as f:
    json.dump(data, f, indent=4)

print(f"更新完成，新的 JSON 文件保存在: {output_json_path}")
