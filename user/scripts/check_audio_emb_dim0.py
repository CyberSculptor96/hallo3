import os
import torch
from tqdm import tqdm

# 设置目标文件夹路径
dir_path = "/wangbenyou/huanghj/data/shunian-hallo3-dataset/audio_emb"

# 创建一个集合来存储第一维的大小
first_dim_sizes = set()

# 遍历该目录下的所有 .pt 文件
for filename in tqdm(os.listdir(dir_path), unit="enrty"):
    if filename.endswith(".pt"):  # 确保只处理 .pt 文件
        file_path = os.path.join(dir_path, filename)
        
        try:
            # 加载 .pt 文件
            tensor = torch.load(file_path, map_location="cpu")
            
            # 确保数据是 tensor 类型
            if isinstance(tensor, torch.Tensor):
                first_dim_sizes.add(tensor.shape[0])  # 记录第一维的大小
            else:
                print(f"[Warning] {filename} does not contain a tensor.")
        except Exception as e:
            print(f"[Error] Failed to load {filename}: {e}")

# 打印所有不同的第一维大小
print(f"Unique first dimension sizes: {first_dim_sizes}")
