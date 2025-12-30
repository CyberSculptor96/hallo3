import os

# 定义路径
input_txt_path = '/wangbenyou/huanghj/workspace/hallo3/evaluation/dataset/HDTF/input.txt'
output_dir = '/wangbenyou/huanghj/workspace/hallo3/evaluation/dataset/HDTF/inputs'
os.makedirs(output_dir, exist_ok=True)

# 读取 input.txt 文件（每行为：sentence@@image_path@@audio_path）
with open(input_txt_path, 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

# 总数据条数
total_data = len(lines)
num_splits = 8
entries_per_file = total_data // num_splits

# 遍历并写入
for i in range(num_splits):
    start_idx = i * entries_per_file
    end_idx = (i + 1) * entries_per_file if i < num_splits - 1 else total_data
    lines_to_write = lines[start_idx:end_idx]

    output_txt_path = os.path.join(output_dir, f"input_{entries_per_file}-{i}.txt")
    with open(output_txt_path, 'w') as f:
        for line in lines_to_write:
            f.write(line + '\n')

    print(f"[✓] 写入 {len(lines_to_write)} 行到 {output_txt_path}")

print(f"✅ 所有数据已处理完毕，总共生成 {num_splits} 个文件。")
