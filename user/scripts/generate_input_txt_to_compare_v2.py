import os
import json
import os.path as osp
import re

# 定义路径
json_file = "/wangbenyou/shunian/workspace/talking_face/video_processing/video_preprocess/Trunk_mass_filtering/test_pipeline/test/video_caption/sample.json"
base_dir = "/wangbenyou/huanghj/workspace/hallo3/output/output_testset-0320/10k-steps"
output_txt_path = "/wangbenyou/huanghj/workspace/hallo3/output/output_sentences.txt"

# 读取 JSON 文件
with open(json_file, 'r') as f:
    json_data = json.load(f)

# 建立 video_folder 到 description_summary 的映射
# video_captions = {osp.splitext(item["image_file"])[0]: item["response"]["choices"][0]["message"]['content']["description_summary"] for item in json_data if "image_file" in item and "response" in item}

video_captions = {}
for item in json_data:
    if "image_file" in item and "response" in item:
        try:
            content = item["response"]["choices"][0]["message"]["content"]
            # 用正则匹配JSON代码块
            # 尝试解析 content 为 JSON
            try:
                content_json = json.loads(content)
                summary = content_json.get("description_summary", "")
            except json.JSONDecodeError:
                # content 是纯文本，从中提取 summary
                match = re.search(r"#### Description Summary\\n(.+?)$", content, re.DOTALL)
                if match:
                    summary = match.group(1)  # 提取JSON部分
                else:
                    summary = "a person is talking"
                    
            video_captions[item["image_file"].replace(".jpg", "")] = summary
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Error processing item {item}: {e}")

# 获取所有子目录的名字
dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

# 生成句子并写入文件
with open(output_txt_path, 'w') as f:
    for dirname in dirs:
        modified_dirname = dirname[::-1].replace("_", "-", 1)[::-1]  # 仅替换最后一个 "_" 为 "-"
        if modified_dirname in video_captions:
            caption = video_captions[modified_dirname]
        else:
            caption = "a person is talking"
            pass
        sentence = f"{caption}@@/wangbenyou/huanghj/workspace/hallo3/examples/test_data-0320/imgs/{dirname}_first_frame.png@@/wangbenyou/huanghj/workspace/hallo3/examples/test_data-0320/audios/{dirname}_first_frame.wav"
        f.write(sentence + "\n")

print(f"Generated {len(dirs)} sentences in {output_txt_path}.")
