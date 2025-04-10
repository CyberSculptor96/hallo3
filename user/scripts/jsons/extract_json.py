import json

# 输入文件路径
input_file = '/wangbenyou/huanghj/workspace/hallo3/json/data_sampled.json'
# 输出文件路径
output_file = '/wangbenyou/huanghj/workspace/hallo3/json/data_sampled_filtered.json'

# 读取原始 JSON 文件
with open(input_file, 'r') as f:
    data = json.load(f)

# 提取所需字段
filtered_data = []
for item in data:
    filtered_item = {
        "id": item.get("id"),
        "video-path": item.get("video-path"),
        "audio-path": item.get("audio-path"),
        "fps": item.get("fps")
    }
    filtered_data.append(filtered_item)

# 将过滤后的数据写入新的 JSON 文件
with open(output_file, 'w') as f:
    json.dump(filtered_data, f, indent=4)

print(f"新文件已保存到: {output_file}")
