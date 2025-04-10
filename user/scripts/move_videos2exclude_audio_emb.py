import os
import shutil
from tqdm import tqdm

# 定义目录路径
videos_dir = '/wangbenyou/huanghj/data/shunian-hallo3-dataset/videos'
audio_emb_dir = '/wangbenyou/huanghj/data/shunian-hallo3-dataset/audio_emb'
videos2_dir = '/wangbenyou/huanghj/data/shunian-hallo3-dataset/videos2'

# 创建videos2目录
os.makedirs(videos2_dir, exist_ok=True)

# 获取audio_emb目录下的所有文件名（不带扩展名）
audio_emb_files = {os.path.splitext(f)[0] for f in os.listdir(audio_emb_dir)}

# 遍历videos目录中的所有软链接文件
for video_link in tqdm(os.listdir(videos_dir), unit="entry"):
    video_path = os.path.join(videos_dir, video_link)
    
    # 检查是否为软链接
    if os.path.islink(video_path):
        # 获取文件名（不带扩展名）
        video_name = os.path.splitext(video_link)[0]
        
        # 如果文件名不在audio_emb目录中，则复制软链接到videos2目录
        if video_name not in audio_emb_files:
            target_path = os.path.join(videos2_dir, video_link)
            os.symlink(os.readlink(video_path), target_path)

print('Finished creating symlinks in videos2 directory.')