import os
import multiprocessing
from tqdm import tqdm

# 定义路径
video_dir = "/wangbenyou/huanghj/data/fastvideo-hallo3-dataset/media"
output_dir = "/wangbenyou/huanghj/workspace/hallo3/evaluation/pytorch_fid/dataset_pair/all_images-real-hallo3_2"

# 确保输出目录存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 获取所有 .mp4 文件，并按名称排序
all_videos = sorted([f for f in os.listdir(video_dir) if f.endswith(".mp4")])
selected_videos = all_videos[-100:]  # 选取前 100 个视频
selected_video_paths = [os.path.join(video_dir, f) for f in selected_videos]  # 构建完整路径

# FFmpeg 提取视频帧的命令模板
def extract_frames(video_path):
    """ 提取视频的所有帧，并存入目标文件夹 """
    video_name = os.path.basename(video_path).split('.')[0]  # 获取视频名称（去掉后缀）
    output_pattern = os.path.join(output_dir, f"{video_name}_%06d.jpg")  # 以6位数命名帧

    # FFmpeg 命令（每秒提取 30 帧，高速处理）
    cmd = f"ffmpeg -i '{video_path}' -vf 'fps=30' -q:v 2 '{output_pattern}' -loglevel error"
    os.system(cmd)  # 执行 FFmpeg 命令

# 进程池处理所有视频
def process_videos():
    num_workers = min(multiprocessing.cpu_count(), 8)  # 限制最多 8 进程，防止 CPU 过载
    with multiprocessing.Pool(processes=num_workers) as pool:
        with tqdm(total=len(selected_video_paths), desc="Extracting Frames", unit="video") as pbar:
            for _ in pool.imap_unordered(extract_frames, selected_video_paths):
                pbar.update(1)  # 每处理完一个视频，进度条更新

if __name__ == "__main__":
    process_videos()
    print("✅ 所有视频帧已成功提取并存储到目标文件夹！")
