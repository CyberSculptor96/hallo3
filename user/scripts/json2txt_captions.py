import json
from pathlib import Path
from tqdm import tqdm

# 读取 JSON 数据
json_path = Path("/wangbenyou/shunian/workspace/talking_face/Talking-Face-Datapipe/7_video_caption/data/test_time/sample/fixed_sample_data_total.json")
output_dir = Path("/wangbenyou/huanghj/data/hallo3-dataset/captions")

# 确保目标目录存在
output_dir.mkdir(parents=True, exist_ok=True)

# 加载 JSON
with json_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

# 遍历 JSON 数据并写入文本文件
for item in tqdm(data, desc="Processing entries", unit="entry"):
    video_path = Path(item['video-path'])
    caption = item['response']['choices'][0]['message']['content']['description_summary']

    # 生成保存路径
    output_file = output_dir / f"{video_path.stem}.txt"

    # 写入 caption
    with output_file.open("w", encoding="utf-8") as f:
        f.write(caption)

print(f"所有 captions 已成功写入 {output_dir}")
