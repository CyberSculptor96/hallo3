import os
import cv2
from pathlib import Path
from glob import glob
from multiprocessing import Pool
from tqdm import tqdm

# 输入输出路径
base_path = Path("/wangbenyou/huanghj/workspace/hallo3/")
# input_dir = base_path / "evaluation/dataset/HDTF/videos_512x512"
input_dir = base_path / "evaluation/dataset/HDTF/outputs/videos"
output_dir = base_path / "evaluation/dataset/HDTF/fframes"
output_dir.mkdir(parents=True, exist_ok=True)

def extract_first_frame(video_path):
    video_path = Path(video_path)
    cap = cv2.VideoCapture(str(video_path))

    success, frame = cap.read()
    if success:
        jpg_path = output_dir / (video_path.stem + ".jpg")
        cv2.imwrite(str(jpg_path), frame)
    cap.release()
    return video_path.name if success else None

def main():
    video_files = sorted(glob(str(input_dir / "*.mp4")))
    print(f"共找到 {len(video_files)} 个视频，开始提取第一帧...")

    with Pool(processes=os.cpu_count()) as pool:
        results = list(tqdm(pool.imap(extract_first_frame, video_files), total=len(video_files)))

    extracted = [r for r in results if r is not None]
    print(f"\n✅ 成功提取第一帧的数量: {len(extracted)} / {len(video_files)}")
    print(f"🖼️ 输出目录：{output_dir}")

if __name__ == "__main__":
    main()
