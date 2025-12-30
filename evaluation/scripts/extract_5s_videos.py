import os
import subprocess
from multiprocessing import Pool, cpu_count
from glob import glob
from tqdm import tqdm

src_dir = "/wangbenyou/huanghj/workspace/hallo3/evaluation/dataset/HDTF/videos_512x512"
dst_dir = "/wangbenyou/huanghj/workspace/hallo3/evaluation/dataset/HDTF/videos_5s"
os.makedirs(dst_dir, exist_ok=True)

NUM_PROC = min(cpu_count(), 32)

def process_video(src_path):
    filename = os.path.basename(src_path)
    dst_path = os.path.join(dst_dir, filename)

    # ffmpeg 命令：重设 fps=25，裁剪前5秒
    command = [
        "ffmpeg",
        "-i", src_path,
        "-r", "25",        # 设置帧率
        "-t", "5",         # 裁剪前 5 秒
        "-c:v", "libx264", # 编码器
        "-y",              # 覆盖输出文件
        dst_path
    ]

    # 静默运行
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return dst_path

def main():
    video_list = glob(os.path.join(src_dir, "*.mp4"))
    print(f"共发现 {len(video_list)} 个视频，开始多进程处理...")

    with Pool(processes=NUM_PROC) as pool:
        list(tqdm(pool.imap(process_video, video_list), total=len(video_list)))

    print("✅ 所有视频已成功转换并保存至:", dst_dir)

if __name__ == "__main__":
    main()
