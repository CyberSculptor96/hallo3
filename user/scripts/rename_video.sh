#!/bin/bash

# 目标目录
TARGET_DIR="/wangbenyou/huanghj/workspace/hallo3/output/output_testset-0320/10k-steps"

# 遍历目标目录中的所有子目录
for dir in "$TARGET_DIR"/*; do
    if [[ -d "$dir" ]]; then
        # 获取子目录名称
        subdir_name=$(basename "$dir")

        # 目标文件路径
        original_file="$dir/000000_with_audio.mp4"
        new_file="$dir/${subdir_name}-10k.mp4"

        # 如果原始文件存在，则进行重命名
        if [[ -f "$original_file" ]]; then
            mv "$original_file" "$new_file"
            echo "已重命名 $original_file 为 $new_file"
        else
            echo "警告：文件 $original_file 不存在，跳过 $subdir_name"
        fi
    fi
done

echo "所有原始视频文件重命名完成！"
