#!/bin/bash

# 进入目标目录
cd /wangbenyou/huanghj/workspace/hallo3/output/output_testset-0320/origin-hallo3 || exit

# 遍历所有子目录
for dir in *; do
    if [[ -d "$dir" ]]; then
        # 查找当前目录下的 mp4 文件
        for file in "$dir"/*.mp4; do
            if [[ -f "$file" ]]; then
                # 提取原文件名（不含扩展名）
                filename=$(basename -- "$file" .mp4)
                # 构造新文件名
                new_name="${filename}-hallo3.mp4"
                # 重命名文件
                mv "$file" "$dir/$new_name"
            fi
        done
    fi
done

echo "所有视频文件后缀已添加 -hallo3！"
