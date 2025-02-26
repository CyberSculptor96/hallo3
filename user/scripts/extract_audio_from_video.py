import os
import json
import subprocess

# 输入的 JSON 文件路径
input_json_file = '/wangbenyou/huanghj/workspace/hallo3/json/data_sampled_filtered.json'

# 输出音频文件保存目录
audio_output_dir = '/wangbenyou/huanghj/workspace/hallo3/user/audios/'

# 读取原始 JSON 文件
with open(input_json_file, 'r') as f:
    data = json.load(f)

# 处理每条记录，提取音频并更新 audio-path
for entry in data:
    # 获取视频文件路径
    video_path = entry['video-path']
    
    # 获取视频文件名（不含扩展名）
    video_filename = os.path.basename(video_path)
    video_name_noext = os.path.splitext(video_filename)[0]
    
    # 生成新的音频文件路径
    audio_filename = f"{video_name_noext}.m4a"
    audio_path = os.path.join(audio_output_dir, audio_filename)

    # 提取音频并保存为 m4a 格式
    cmd = [
        'ffmpeg', 
        '-i', video_path,  # 输入视频文件
        '-vn',             # 不处理视频
        '-acodec', 'aac',  # 使用 AAC 音频编解码器
        '-b:a', '192k',    # 设置音频比特率
        audio_path         # 输出音频文件路径
    ]
    
    try:
        # 执行音频提取命令
        subprocess.run(cmd, check=True)
        print(f"音频已提取：{audio_path}")

        # 更新原 JSON 文件中的 audio-path 字段
        entry['audio-path'] = audio_path
    
    except subprocess.CalledProcessError as e:
        print(f"提取音频失败：{video_path} 错误信息：{e}")

# 保存更新后的 JSON 文件
output_json_file = '/wangbenyou/huanghj/workspace/hallo3/json/data_sampled_filtered_updated.json'
with open(output_json_file, 'w') as f:
    json.dump(data, f, indent=4)

print(f"已保存更新后的 JSON 文件：{output_json_file}")
