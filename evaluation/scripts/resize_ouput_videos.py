import os
import subprocess
from multiprocessing import Pool
from glob import glob
from pathlib import Path
from tqdm import tqdm

# 原始路径和目标路径
input_dir = Path("/wangbenyou/huanghj/workspace/hallo3/evaluation/dataset/HDTF/outputs/videos")
output_dir = Path("/wangbenyou/huanghj/workspace/hallo3/evaluation/dataset/HDTF/outputs/videos_512x512")
output_dir.mkdir(parents=True, exist_ok=True)

def resize_video(video_path):
    video_path = Path(video_path)
    output_path = output_dir / video_path.name

    # ffmpeg 转换命令
    command = [
        "ffmpeg",
        "-i", str(video_path),
        "-vf", "scale=512:512",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",  # 保持较高画质
        "-y",  # 自动覆盖
        str(output_path)
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return video_path.name

def main():
    video_files = sorted(glob(str(input_dir / "*.mp4")))
    print(f"找到 {len(video_files)} 个视频，开始转换至 512x512 ...")

    with Pool(processes=os.cpu_count()) as pool:
        list(tqdm(pool.imap(resize_video, video_files), total=len(video_files)))

    print(f"\n✅ 所有视频已成功转换并保存至：{output_dir}")

if __name__ == "__main__":
    main()
