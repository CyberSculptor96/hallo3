import os

def main():
    # 1. 定义音频目录、图像目录以及输出的文本文件路径
    audio_dir = "/wangbenyou/huanghj/workspace/hallo3/examples/test_data-0331/audios"
    img_dir = "/wangbenyou/huanghj/workspace/hallo3/examples/test_data-0331/imgs"
    output_txt = "/wangbenyou/huanghj/workspace/hallo3/examples/test_data-0331/list.txt"
    
    # 2. 获取音频文件列表（只要.wav后缀）
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith(".wav")]
    audio_files.sort()
    
    # 3. 打开输出文本文件
    with open(output_txt, "w", encoding="utf-8") as out_f:
        for audio_file in audio_files:
            # 去掉 .wav 后缀以便拼接图像文件
            base_name = audio_file[:-4]  # "videovideoXXX-sceneXX_scene1"
            
            # 拼接出图像文件名
            img_file = base_name + "_first_frame.png"
            
            # 组合完整路径
            audio_path = os.path.join(audio_dir, audio_file)
            img_path = os.path.join(img_dir, img_file)
            
            # 如果需要检查文件是否真的存在，可以添加检查：
            # if not os.path.exists(img_path):
            #     print(f"[警告] 找不到对应的图像文件: {img_path}")
            #     continue
            
            # 4. 输出一行格式：a person is talking@@imgpath@@audiopath
            line = f"a person is talking@@{img_path}@@{audio_path}"
            out_f.write(line + "\n")
    
    print(f"[完成] 已生成文本文件: {output_txt}")

if __name__ == "__main__":
    main()
