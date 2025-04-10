#!/bin/bash

# 进入目标目录
cd /wangbenyou/huanghj/workspace/hallo3/output/output_testset-0320/origin-hallo3 || exit

# 遍历所有文件夹
for dir in *; do
    if [[ -d "$dir" ]]; then
        # 提取修改后的目录名称
        new_name=$(echo "$dir" | sed -E 's/_first_frame.*//')
        
        # 重命名文件夹
        if [[ "$dir" != "$new_name" ]]; then
            mv "$dir" "$new_name"
        fi

        # 重命名子目录下的视频文件
        if [[ -f "$new_name/000000_with_audio.mp4" ]]; then
            mv "$new_name/000000_with_audio.mp4" "$new_name/$new_name.mp4"
        fi
    fi
done

echo "所有文件夹和视频文件重命名完成！"
