"""
将分散在不同文件夹下的视频帧图片整合到一个文件夹中。
"""
import os
import shutil
import multiprocessing
from tqdm import tqdm

# 定义源目录和目标目录
source_dir = '/wangbenyou/huanghj/workspace/hallo3/evaluation/syncnet_python/output/hallo3'
target_dir = '/wangbenyou/huanghj/workspace/hallo3/evaluation/syncnet_python/output/all_images'

# 如果目标文件夹不存在，则创建
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

version = 2
if version == 2:
    # 获取所有子目录
    subdirs = [os.path.join(source_dir, subdir) for subdir in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, subdir))]

    # 获取所有图片文件路径
    image_files = []
    for subdir in subdirs:
        for file in os.listdir(subdir):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                image_files.append(os.path.join(subdir, file))

    # 进度条包装
    def copy_file(source_file):
        """ 复制文件到目标文件夹，并避免文件名冲突 """
        file_name = os.path.basename(source_file)
        target_file = os.path.join(target_dir, file_name)

        # 避免文件名冲突
        base_name, ext = os.path.splitext(file_name)
        counter = 1
        while os.path.exists(target_file):
            target_file = os.path.join(target_dir, f"{base_name}_{counter}{ext}")
            counter += 1

        # 复制文件
        shutil.copy2(source_file, target_file)
        return file_name  # 用于进度条更新

    # 使用多进程进行文件复制
    def process_images():
        num_workers = min(multiprocessing.cpu_count(), 8)
        with multiprocessing.Pool(processes=num_workers) as pool:
            with tqdm(total=len(image_files), desc="Processing Images", unit="file") as pbar:
                for _ in pool.imap_unordered(copy_file, image_files):
                    pbar.update(1)

    if __name__ == "__main__":
        process_images()
        print("✅ 所有图片已成功汇总到目标文件夹！")

elif version == 1:
    # 遍历 source_dir 目录下的所有子目录
    for subdir in os.listdir(source_dir):
        subdir_path = os.path.join(source_dir, subdir)

        # 确保它是一个目录
        if os.path.isdir(subdir_path):
            # 遍历该子目录中的所有文件
            for file in os.listdir(subdir_path):
                # 只处理图片文件
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                    source_file = os.path.join(subdir_path, file)
                    target_file = os.path.join(target_dir, file)

                    # 避免文件名冲突
                    base_name, ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(target_file):
                        target_file = os.path.join(target_dir, f"{base_name}_{counter}{ext}")
                        counter += 1
                    
                    # 复制文件到目标文件夹
                    shutil.copy2(source_file, target_file)

    print("所有图片已成功汇总到目标文件夹！")
