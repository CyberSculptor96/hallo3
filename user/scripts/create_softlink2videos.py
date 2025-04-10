import json
import os
from pathlib import Path
from tqdm import tqdm

# 读取 JSON 数据
json_path = Path("/wangbenyou/shunian/workspace/talking_face/Talking-Face-Datapipe/7_video_caption/data/test_time/sample/fixed_sample_data_total.json")
videos_dir = Path("/wangbenyou/huanghj/data/hallo3-dataset-dev/videos")

# 确保目标目录存在
videos_dir.mkdir(parents=True, exist_ok=True)

# 加载 JSON
with json_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

# 遍历 JSON 数据并创建软链接
for item in tqdm(data, desc="Processing entries", unit="entry"):
    video_path = Path(item['video-path'])
    
    # 获取源文件的绝对路径
    if video_path.exists():
        # 构建软链接的目标路径
        target_link = videos_dir / video_path.name

        # 如果目标文件不存在，则创建软链接
        if not target_link.exists():
            os.symlink(video_path, target_link)
        else:
            print(f"软链接已存在：{target_link}")
    else:
        print(f"源文件不存在：{video_path}")

print("所有视频文件的软链接已成功创建！")
