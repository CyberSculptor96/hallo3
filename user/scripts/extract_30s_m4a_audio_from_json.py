import os
import json
import subprocess

def main():
    # 1. JSON 文件路径
    json_file = "/wangbenyou/huanghj/workspace/hallo3/examples/test_data-0324/fps24_121frames_in_label.json"
    
    # 2. 视频所在文件夹
    video_dir = "/wangbenyou/huanghj/workspace/hallo3/examples/test_data-0331/videos"
    
    # 3. 输出音频文件夹
    audio_output_dir = "/wangbenyou/huanghj/workspace/hallo3/examples/test_data-0331/audios"
    
    # 如果输出文件夹不存在，创建它
    if not os.path.exists(audio_output_dir):
        os.makedirs(audio_output_dir, exist_ok=True)

    # 4. 读取 JSON 文件
    with open(json_file, "r", encoding="utf-8") as f:
        data_list = json.load(f)
    
    # 5. 建立从视频文件名(带后缀)到对应字典信息的映射
    video_map = {}
    for item in data_list:
        video_path = item.get("video-path", "")
        if video_path:
            # 取出视频文件名（不含路径）
            base_name = os.path.basename(video_path)  # e.g. "videovideoYMz91i7B2kw-scene2_scene1.mp4"
            video_map[base_name] = item

    # 6. 遍历目录中的所有 mp4 文件，尝试匹配
    for filename in os.listdir(video_dir):
        if filename.endswith(".mp4"):
            # 如果在映射表中找到了对应信息
            if filename in video_map:
                info_dict = video_map[filename]
                start_time = info_dict.get("start-time", 0)  # 默认值 0
                original_audio = info_dict.get("original-audio", "")
                
                # 构造输出音频路径
                # 去掉 .mp4 扩展名，改为 .m4a
                audio_filename = os.path.splitext(filename)[0] + ".m4a"
                output_audio_path = os.path.join(audio_output_dir, audio_filename)

                # 如果 original_audio 为空，跳过
                if not original_audio:
                    print(f"[警告] {filename} 的 original-audio 为空，无法截取音频。")
                    continue

                # 7. 调用 ffmpeg 截取 30 秒音频
                # 这里使用 -c copy 直接拷贝音频，不进行转码。若需要转码，可改为 -c:a aac 等。
                cmd = [
                    "ffmpeg",
                    "-ss", str(start_time),     # 截取起始时间
                    "-t", "30",                 # 截取 30 秒
                    "-i", original_audio,       # 原始音频路径
                    "-c", "copy",               # 不进行重新编码
                    "-y",                       # 覆盖输出文件
                    output_audio_path
                ]

                print(f"正在处理: {filename}\n命令: {' '.join(cmd)}\n")
                try:
                    subprocess.run(cmd, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"[错误] 执行 ffmpeg 失败: {e}")
            else:
                # JSON 中未找到匹配，视情况选择打印提示或忽略
                print(f"[提示] 找不到 {filename} 对应的 JSON 信息，跳过。")

if __name__ == "__main__":
    main()
