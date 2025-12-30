import os
import glob
import subprocess
from multiprocessing import Pool, cpu_count
from functools import partial
from tqdm import tqdm

# 输入输出路径配置
video_dir = "/wangbenyou/huanghj/workspace/hallo3/evaluation/dataset/HDTF/videos_512x512"
output_dir = "/wangbenyou/huanghj/workspace/hallo3/evaluation/dataset/HDTF/audios"
os.makedirs(output_dir, exist_ok=True)

NUM_PROC = min(cpu_count(), 32)

# 每个视频处理函数
def extract_audio(video_path, output_dir):
    filename = os.path.basename(video_path)
    name, _ = os.path.splitext(filename)
    output_path = os.path.join(output_dir, f"{name}.wav")

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-t", "5",               # 前5秒
        "-ar", "16000",          # 采样率16kHz
        "-ac", "1",              # 单声道
        "-vn",                   # 不要视频
        output_path
    ]

    try:
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# tqdm 兼容的多进程 wrapper
def tqdm_pool_map(func, iterable, total, processes):
    with Pool(processes=processes) as pool:
        results = []
        for result in tqdm(pool.imap_unordered(func, iterable), total=total):
            results.append(result)
        return results

# 主入口
if __name__ == "__main__":
    video_paths = sorted(glob.glob(os.path.join(video_dir, "*.mp4")))
    print(f"Found {len(video_paths)} videos.")

    # 使用 partial 绑定输出目录参数
    wrapped_func = partial(extract_audio, output_dir=output_dir)

    # tqdm + multiprocessing
    tqdm_pool_map(wrapped_func, video_paths, total=len(video_paths), processes=NUM_PROC)

    print("✅ All done.")
