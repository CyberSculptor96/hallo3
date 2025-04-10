import os
from tqdm import tqdm

# 定义路径
base_dir = "/wangbenyou/huanghj/workspace/hallo3/output/output_testset-0320"
input_txt_path = "/wangbenyou/huanghj/workspace/hallo3/examples/inference/input_testset_40-3.txt"

# 读取 input_testset_40-1.txt 文件中的所有前缀
with open(input_txt_path, 'r') as f:
    valid_prefixes = list(line.strip() for line in f if line.strip())

# 遍历 base_dir 下的所有子目录
for subdir in tqdm(os.listdir(base_dir)):
    full_subdir_path = os.path.join(base_dir, subdir)
    
    # 确保是目录
    if os.path.isdir(full_subdir_path):
        
        # 查找 "_first_frame" 之前的前缀
        if "_first_frame" in subdir:
            prefix = subdir.split("_first_frame")[0]
            
            # 检查前缀是否在 input_testset_40-1.txt 中
            hit = [prefix in valid_prefixes[i] for i in range(len(valid_prefixes))]
            if True:
                new_subdir_name = f"{prefix}-6k"
                new_subdir_path = os.path.join(base_dir, new_subdir_name)
                
                # 重命名目录
                os.rename(full_subdir_path, new_subdir_path)
                print(f"Renamed: {subdir} -> {new_subdir_name}")

print("Renaming process completed.")
