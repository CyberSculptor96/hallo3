import json
import os

# 定义文件路径
input_json_path = '/wangbenyou/huanghj/workspace/hallo3/examples/test_data-0320/fps24_121frames_in_label.json'
output_dir = '/wangbenyou/huanghj/workspace/hallo3/examples/inference/'

# 读取 JSON 文件
with open(input_json_path, 'r') as f:
    data = json.load(f)

# 总数据条数
total_data = len(data)

# 每个文件包含的条目数
entries_per_file = 40

# 计算需要输出的文件数
# num_files = total_data // entries_per_file
num_files = 1

# 遍历文件编号 0-7，每个文件写入22条数据
for i in range(num_files):
    i += 4
    # 每次提取22条数据
    data_to_process = data[i * entries_per_file:(i + 1) * entries_per_file]
    
    # 输出文件路径
    output_txt_path = f"{output_dir}input_testset_40-{i}.txt"
    
    # 写入到对应的 TXT 文件
    with open(output_txt_path, 'w') as f:
        for item in data_to_process:
            # 提取相关字段
            audio_path = item['audio-path']
            first_frame_path = item['first-frame-path']
            sentence = "a person is talking"  # 根据要求的句子

            # 格式化并写入
            line = f"{sentence}@@{first_frame_path}@@{audio_path}\n"
            f.write(line)
    
    # 打印确认消息
    print(f"数据已成功写入到 {output_txt_path}")

# 打印最终消息
print("所有数据已处理完成，输出了 8 个文件。")
