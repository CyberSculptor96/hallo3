from pathlib import Path

# 两个路径
dir_a = Path("/wangbenyou/huanghj/workspace/hallo3/evaluation/dataset/HDTF/outputs/videos")
dir_b = Path("/wangbenyou/huanghj/workspace/hallo3/evaluation/dataset/HDTF/videos_512x512")

# 输出路径
output_txt = Path("missing_in_outputs.txt")

# 获取两个目录下所有 .mp4 文件名（不带路径）
files_a = {p.name for p in dir_a.glob("*.mp4")}
files_b = {p.name for p in dir_b.glob("*.mp4")}

# 查找只在 B 中存在的文件
only_in_b = sorted(files_b - files_a)

# 写入文件
with open(output_txt, "w") as f:
    for filename in only_in_b:
        f.write(f"{filename}\n")

print(f"✅ 共发现 {len(only_in_b)} 个视频仅存在于 videos_512x512 目录中")
print(f"📄 已保存文件名列表至: {output_txt.resolve()}")
