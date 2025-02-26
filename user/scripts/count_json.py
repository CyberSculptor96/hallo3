import os
import json

def count_json(json_path):
    # 加载 JSON 文件
    with open(json_path, "r") as f:
        json_data = json.load(f)
    
    print(f"len of json_files: {len(json_data)}")


if __name__ == "__main__":
    base_path = "/wangbenyou/huanghj/workspace/sora/FastVideo-shunian-0212"
    # json_path = os.path.join(base_path, "/wangbenyou/shunian/workspace/talking_face/Talking-Face-Datapipe/7_video_caption/data/test_time/sample/fixed_sample.json")
    json_path = os.path.join(base_path, "/wangbenyou/shunian/workspace/talking_face/video_processing/video_filtering/sample_diverse_data/data_sampled.json")
    
    count_json(json_path)
