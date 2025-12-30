#!/bin/bash

# 设置路径
root_dir="/wangbenyou/huanghj/workspace/hallo3/evaluation/dataset/HDTF/outputs"
output_dir="${root_dir}/videos"

# 创建目标目录（如果不存在）
mkdir -p "$output_dir"

# 遍历 card0 和 card1 目录
for card in card4 card5 card6 card7; do
    card_path="${root_dir}/${card}"
    
    # 遍历每个子目录
    for subdir in "$card_path"/*; do
        if [ -d "$subdir" ]; then
            # 获取子目录名
            dirname=$(basename "$subdir")
            
            # 提取前缀
            prefix=${dirname%%-*}
            
            # 源视频路径
            src_video="${subdir}/000000_with_audio.mp4"
            
            # 目标视频路径
            dst_video="${output_dir}/${prefix}.mp4"
            
            if [ -f "$src_video" ]; then
                echo "Moving $src_video -> $dst_video"
                mv "$src_video" "$dst_video"
            else
                echo "⚠️  Warning: $src_video not found, skipping."
            fi
        fi
    done
done

echo "✅ All videos moved and renamed to $output_dir"
