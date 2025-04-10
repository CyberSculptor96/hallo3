import json
from tqdm import tqdm

# 输入文件路径
input_json_path = '/wangbenyou/huanghj/workspace/hallo3/json/fixed_sample_data_total.json'
# 输出文件路径
output_json_path = '/wangbenyou/huanghj/workspace/hallo3/json/fixed_sample_data_total_modified.json'

# 定义需要替换的前缀和新前缀
old_prefix = '/sds_wangby/datasets_dir/datasets/shunian/workspace/talking_face/Talking-Face-Datapipe/outputs/common/'
new_prefix = '/sskj-prod/gzs/test/shunian/data/talkingface/'

# 加载 JSON 文件
with open(input_json_path, 'r') as f:
    data = json.load(f)

for entry in tqdm(data, desc="Processing entries", unit="entry"):
    if "video-path" in entry:
        entry['video-path'] = entry['video-path'].replace(old_prefix, new_prefix)

with open(output_json_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"修改后的 JSON 文件已保存到: {output_json_path}")