import json
import os

# 定义文件路径
data_sampled_json_path = '/wangbenyou/shunian/workspace/talking_face/video_processing/video_filtering/sample_diverse_data/data_sampled.json'
fixed_sample_json_path = '/wangbenyou/shunian/workspace/talking_face/Talking-Face-Datapipe/7_video_caption/data/test_time/sample/fixed_sample.json'
output_dir = '/wangbenyou/huanghj/workspace/hallo3/examples/inference/'

# 读取 data_sampled.json
with open(data_sampled_json_path, 'r') as f:
    data_sampled = json.load(f)

# 读取 fixed_sample.json
with open(fixed_sample_json_path, 'r') as f:
    caption_data = json.load(f)

# 构建 caption 查找表 (使用 video_folder 作为 key)
caption_lookup = {
    item["video_folder"]: item["response"]["choices"][0]["message"]["content"]["comprehensive_summary"]["overall_narrative"]
    for item in caption_data
}

# 总数据条数
total_data = len(data_sampled)

# 每个文件包含的条目数
entries_per_file = 10

start_index = 8 * 22  # 176

# 计算需要输出的文件数
num_files = 8

# 遍历文件编号 0-7，每个文件写入22条数据
for i in range(num_files):
    # 每次提取 22 条数据
    data_to_process = data_sampled[start_index + i * entries_per_file: start_index + (i + 1) * entries_per_file]

    # 输出文件路径
    output_txt_path = f"{output_dir}input_testset_caption_10-{i}.txt"

    # 写入到对应的 TXT 文件
    with open(output_txt_path, 'w') as f:
        for item in data_to_process:
            # 获取 id，匹配 caption
            video_id = item['id']
            caption = caption_lookup.get(video_id, "No caption available")  # 默认值防止找不到匹配项
            
            # 如果没有匹配到 caption，则记录该条数据和其对应的 caption json 文件内容
            if caption == "No caption available":
                print(f"未找到 caption 的数据（ID: {video_id}）：")
                print("对应的 caption JSON 文件内容：")
                print(json.dumps(caption_lookup.get(video_id), indent=4))  # 打印整个对应的 caption json 文件内容
                print()
                
            # 提取路径
            audio_path = item['audio-path']
            first_frame_path = item['first-frame-path']
            
            # 组织格式并写入
            line = f"{caption}@@{first_frame_path}@@{audio_path}\n"
            f.write(line)

    # 打印确认消息
    print(f"数据已成功写入到 {output_txt_path}")

# 打印最终消息
print("所有数据已处理完成，输出了 8 个文件。")
