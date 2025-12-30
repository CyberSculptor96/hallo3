import os
import cv2
from collections import defaultdict
import os.path as osp

# 视频文件所在目录
base_path = "/wangbenyou/huanghj/workspace/hallo3/"
# video_dir = osp.join(base_path, "evaluation/dataset/HDTF/outputs/videos")
video_dir = osp.join(base_path, "evaluation/dataset/HDTF/videos_5s")

# 初始化统计变量
fps_set = set()
frame_counts = defaultdict(list)

# 遍历目录下的所有 mp4 文件
for filename in os.listdir(video_dir):
    if filename.endswith(".mp4"):
        filepath = os.path.join(video_dir, filename)
        cap = cv2.VideoCapture(filepath)

        if not cap.isOpened():
            print(f"❌ Failed to open video: {filename}")
            continue

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        fps_set.add(fps)
        frame_counts[total_frames].append(filename)

        cap.release()

# 打印 fps 检查结果
print("✅ 所有视频的 fps 值集合:")
print(fps_set)
if fps_set == {25.0}:
    print("✅ All videos have fps == 25")
else:
    print("⚠️ Not all videos have fps == 25")

# 打印帧数统计信息
print("\n📊 视频帧数分布 (帧数 -> 文件数):")
for frame_count, files in sorted(frame_counts.items()):
    print(f"{frame_count} frames -> {len(files)} video(s)")
