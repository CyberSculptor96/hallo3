import os
import cv2
import matplotlib.pyplot as plt
import multiprocessing
from tqdm import tqdm
import numpy as np

def get_video_info(video_path):
    """
    获取视频的帧数和秒数
    :param video_path: 视频文件路径
    :return: (视频路径, 帧数, 秒数) 或 None（失败时）
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"无法打开视频文件: {video_path}")
            return None

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 总帧数
        fps = cap.get(cv2.CAP_PROP_FPS)  # 帧率
        cap.release()

        if fps == 0:
            print(f"视频 {video_path} 的帧率为 0，跳过。")
            return None

        duration = frame_count / fps  # 视频总秒数
        return (video_path, frame_count, duration)
    except Exception as e:
        print(f"处理 {video_path} 时出错: {e}")
        return None

def plot_histogram(data, title, xlabel, ylabel, bins=50):
    """
    绘制直方图
    :param data: 数据列表
    :param title: 图表标题
    :param xlabel: x 轴标签
    :param ylabel: y 轴标签
    :param bins: 直方图的柱子数量
    """
    plt.figure()
    plt.hist(data, bins=bins, edgecolor='black')

    # plt.xticks(np.linspace(min(data), max(data), num=20, dtype=int)) 
    counts, bin_edges, _ = plt.hist(data, bins=bins, edgecolor='black')

    # 找到最高的 bin
    peak_bin_index = np.argmax(counts)  # 获取最大值索引
    peak_bin_min = bin_edges[peak_bin_index]  # bin 的起始值
    peak_bin_max = bin_edges[peak_bin_index + 1]  # bin 的结束值

    # 打印峰值所在 bin 的范围
    print(f"Peak Bin Range: {peak_bin_min:.2f} - {peak_bin_max:.2f}")

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(f"./{xlabel}-testset.png")

def process_videos_parallel(video_paths, num_workers=8):
    """
    使用多进程并行获取视频信息
    :param video_paths: 视频文件列表
    :param num_workers: 进程数量
    :return: 帧数列表, 时长列表
    """
    frame_counts = []
    durations = []

    with multiprocessing.Pool(processes=num_workers) as pool:
        results = list(tqdm(pool.imap(get_video_info, video_paths), total=len(video_paths), unit="video"))

    # 过滤掉 None 结果，并整理数据
    for result in results:
        if result is not None:
            _, frame_count, duration = result
            frame_counts.append(frame_count)
            durations.append(duration)

    return frame_counts, durations

def main():
    # 视频文件夹路径
    # folder_path = "/wangbenyou/huanghj/data/hallo3-dataset/videos"
    folder_path = "/wangbenyou/huanghj/workspace/hallo3/output/output_testset"

    use_cache = True

    if use_cache:
        frame_counts_file = "./nps/frame_counts-testset.npy"
        durations_file = "./nps/durations-testset.npy"
    else:
        frame_counts_file = ""
        durations_file = ""

    if os.path.exists(frame_counts_file) and os.path.exists(durations_file):
        print("Loading cached data...")
        frame_counts = np.load(frame_counts_file)
        durations = np.load(durations_file)
    else:
        # 获取所有 .mp4 文件路径
        # video_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".mp4")]
        video_paths = [
            os.path.join(root, f)
            for root, _, files in os.walk(folder_path)
            for f in files if f.endswith(".mp4")
        ]

        if not video_paths:
            print("没有找到任何 .mp4 文件，退出程序。")
            return

        print(f"检测到 {len(video_paths)} 个视频文件，开始处理...")

        # 使用多进程获取视频信息
        frame_counts, durations = process_videos_parallel(video_paths, num_workers=multiprocessing.cpu_count())

        if not frame_counts or not durations:
            print("未能成功处理任何视频。")
            return

        # 保存数据到本地
        np.save(frame_counts_file, frame_counts)
        np.save(durations_file, durations)
        print("Processing complete. Data cached for future use.")

    # 打印统计信息
    print(f"总视频数量: {len(frame_counts)}")
    print(f"帧数范围: {min(frame_counts)} - {max(frame_counts)}")
    print(f"秒数范围: {min(durations):.2f} - {max(durations):.2f}")

    # 绘制帧数直方图
    plot_histogram(frame_counts, "Video Frame Count Distribution", "Frame Count", "Number of Videos")

    # 绘制秒数直方图
    plot_histogram(durations, "Video Duration Distribution", "Duration (seconds)", "Number of Videos")

if __name__ == "__main__":
    main()
