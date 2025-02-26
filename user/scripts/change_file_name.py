import os
import re

# 定义路径
base_dir = '/wangbenyou/huanghj/workspace/hallo3/output_testset/'

# 获取所有文件夹名
folder_names = os.listdir(base_dir)

version = 2
if version == 2:
    # 遍历每个文件夹
    for folder_name in folder_names:
        folder_path = os.path.join(base_dir, folder_name)
        
        # 确保是文件夹
        if os.path.isdir(folder_path):
            # 处理文件夹名，确保 "videovideo" 变成 "video"
            new_folder_name = re.sub(r'^video', '', folder_name)  # 替换首个 'videovideo' 为 'video'
            new_folder_path = os.path.join(base_dir, new_folder_name)

            if new_folder_name != folder_name:  # 只有当名字发生变化时才重命名
                os.rename(folder_path, new_folder_path)
                print(f"文件夹重命名: {folder_name} -> {new_folder_name}")
            else:
                print(f"文件夹 {folder_name} 无需修改")
            
            # 修改文件夹内的视频文件名
            for file in os.listdir(new_folder_path):
                if file.endswith('.mp4'):
                    old_file_path = os.path.join(new_folder_path, file)
                    new_file_name = new_folder_name + '.mp4'
                    new_file_path = os.path.join(new_folder_path, new_file_name)

                    if new_file_name != file:  # 只有当名字发生变化时才重命名
                        os.rename(old_file_path, new_file_path)
                        print(f"视频文件重命名: {file} -> {new_file_name}")
                    else:
                        print(f"视频文件 {file} 无需修改")
elif version == 1:
    # 遍历每个文件夹
    for folder_name in folder_names:
        folder_path = os.path.join(base_dir, folder_name)
        
        # 检查是否为文件夹
        if os.path.isdir(folder_path):
            # 使用正则表达式提取新的文件夹名（xxx-seed_yyy格式）
            if '_first_frame-' in folder_name and '-seed_' in folder_name:
                new_folder_name = folder_name.split('_first_frame-')[0] + '-seed' + folder_name.split('-seed_')[1]
                new_folder_path = os.path.join(base_dir, new_folder_name)
                
                # 重命名文件夹
                os.rename(folder_path, new_folder_path)
                print(f"文件夹已重命名：{folder_path} -> {new_folder_path}")
                
                # 在文件夹下查找对应的视频文件
                for file in os.listdir(new_folder_path):
                    if file.endswith('_with_audio.mp4'):
                        # 构建新视频文件名
                        new_file_name = new_folder_name + '.mp4'
                        old_file_path = os.path.join(new_folder_path, file)
                        new_file_path = os.path.join(new_folder_path, new_file_name)
                        
                        # 重命名视频文件
                        os.rename(old_file_path, new_file_path)
                        print(f"视频文件已重命名：{old_file_path} -> {new_file_path}")
            else:
                print(f"文件夹名格式不符合要求：{folder_name}")

