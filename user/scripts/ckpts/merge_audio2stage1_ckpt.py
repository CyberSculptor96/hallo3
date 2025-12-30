import torch
import time
# 路径设置
source_path = "/wangbenyou/huanghj/workspace/hallo3/stage-1/train-stage-1-04-19-05-06/1/mp_rank_00_model_states.pt"
audio_path = "/wangbenyou/huanghj/workspace/hallo3/pretrained_models/hallo3/1/mp_rank_00_model_states.pt"
output_path = "/wangbenyou/huanghj/workspace/hallo3/merged_model_states.pt"

# 加载 state_dicts
start = time.time()
src = torch.load(source_path, map_location="cpu")
end = time.time()
print(f"加载源模型耗时: {end - start:.2f}秒")

start = time.time()
audio_src = torch.load(audio_path, map_location="cpu")
end = time.time()
print(f"加载含有audio键的模型耗时: {end - start:.2f}秒")

# 获取原始模型字典
src_sd = src["module"]
audio_sd = audio_src["module"]
print(f"原始模型的权重数量: {len(src_sd)}")
print(f"含有audio键的模型的权重数量: {len(audio_sd)}")

# 1️⃣ 删除以 conditioner. 和 first_stage_model. 开头的 key
filtered_sd = {
    k: v for k, v in src_sd.items()
    if not (k.startswith("conditioner.") or k.startswith("first_stage_model."))
}

# 2️⃣ 提取 audio 相关的字段
audio_fields = {k: v for k, v in audio_sd.items() if "audio" in k}

# 合并字典
merged_sd = {**filtered_sd, **audio_fields}

# 更新 src 的 module
src["module"] = merged_sd

# 保存到新的文件
start = time.time()
torch.save(src, output_path)
end = time.time()
print(f"保存新模型耗时: {end - start:.2f}秒")

print(f"新模型权重已保存至: {output_path}")
print(f"新模型的权重数量: {len(merged_sd)}")
