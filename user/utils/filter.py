import json
import subprocess
import multiprocessing
from tqdm import tqdm  # 用于进度条

# JSON 文件路径
json_file = "./data/hallo3.json"
output_file = "./data/hallo3-55f.json"

def get_frame_count(video_path):
    """使用 ffprobe 获取视频的帧数"""
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-count_frames", "-show_entries", "stream=nb_read_frames",
        "-of", "default=nokey=1:noprint_wrappers=1", video_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return int(result.stdout.strip())
    except Exception as e:
        print(f"❌ 无法获取视频 {video_path} 的帧数: {e}")
        return 0  # 发生错误时，默认帧数为 0

def process_entry(entry):
    """处理 JSON 中的单个视频条目，返回符合条件的项"""
    if get_frame_count(entry["video_path"]) >= 55:
        return entry  # 符合要求
    return None  # 不符合要求

def process_with_progress(data):
    """多进程处理，并添加 tqdm 进度条"""
    num_workers = min(32, multiprocessing.cpu_count())  # 限制最多 8 进程
    with multiprocessing.Pool(processes=num_workers) as pool:
        # 使用 tqdm 包装 pool.imap 以显示进度条
        results = list(tqdm(pool.imap(process_entry, data), total=len(data), desc="⏳ 处理中", ncols=80))

    # 过滤掉 None（即不符合要求的）
    return [entry for entry in results if entry]

if __name__ == "__main__":
    # 读取 JSON 文件
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 运行处理任务（带进度条）
    filtered_data = process_with_progress(data)

    # 保存过滤后的 JSON 文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=4, ensure_ascii=False)

    print(f"✅ 过滤完成！有效视频数: {len(filtered_data)}，结果已保存至 {output_file}")
