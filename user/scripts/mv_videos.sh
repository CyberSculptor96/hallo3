#!/bin/bash

# 定义源目录和目标目录
SRC_DIR="/wangbenyou/huanghj/workspace/hallo3/output/output_testset-0320/origin-hallo3"
DEST_DIR="/wangbenyou/huanghj/workspace/hallo3/output/output_testset-0320/10k-steps"

# 遍历源目录中的所有子目录
for dir in "$SRC_DIR"/*; do
    if [[ -d "$dir" ]]; then
        # 获取子目录名称
        subdir_name=$(basename "$dir")

        # 检查目标目录下是否存在同名的子目录
        if [[ -d "$DEST_DIR/$subdir_name" ]]; then
            # 查找该子目录下的 mp4 文件
            for file in "$dir"/*.mp4; do
                if [[ -f "$file" ]]; then
                    # 移动文件到对应的目标子目录
                    mv "$file" "$DEST_DIR/$subdir_name/"
                    echo "已移动 $file 到 $DEST_DIR/$subdir_name/"
                fi
            done
        else
            echo "警告：目标目录 $DEST_DIR/$subdir_name 不存在，跳过移动 $subdir_name"
        fi
    fi
done

echo "所有视频文件已成功移动到对应子目录！"
