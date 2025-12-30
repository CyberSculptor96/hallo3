#!/bin/bash

src_root="/wangbenyou/huanghj/workspace/hallo3/output/output_testset-0320/10k-steps"
dst_10k="/wangbenyou/huanghj/workspace/hallo3/evaluation/dataset/TalkVid/outputs/output_10k"
dst_hallo3="/wangbenyou/huanghj/workspace/hallo3/evaluation/dataset/TalkVid/outputs/ouput_hallo3"  # 注意：你这里拼写错了 output 为 ouput，是否需要更正？

# 创建目标目录（如果不存在）
mkdir -p "$dst_10k"
mkdir -p "$dst_hallo3"

# 遍历每个子目录
for dir in "$src_root"/*; do
    if [ -d "$dir" ]; then
        # 查找 .mp4 文件数
        count=$(find "$dir" -maxdepth 1 -type f -name "*.mp4" | wc -l)
        if [ "$count" -eq 2 ]; then
            # 找出两个符合规则的文件并复制
            for file in "$dir"/*.mp4; do
                filename=$(basename "$file")
                if [[ "$filename" == *"-10k.mp4" ]]; then
                    cp "$file" "$dst_10k/"
                elif [[ "$filename" == *"-hallo3.mp4" ]]; then
                    cp "$file" "$dst_hallo3/"
                fi
            done
        fi
    fi
done

echo "拷贝完成 ✅"
