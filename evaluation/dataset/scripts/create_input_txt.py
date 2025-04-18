import os

# 配置路径
base_path = "/wangbenyou/huanghj/workspace/hallo3/"
img_dir = "evaluation/dataset/HDTF/first_frames_176"
audio_dir = "evaluation/dataset/HDTF/audios_5s"
output_txt = "input.txt"

# 获取并排序所有文件名（去后缀）
img_files = sorted([f for f in os.listdir(img_dir) if f.endswith(".jpg")])
audio_files = sorted([f for f in os.listdir(audio_dir) if f.endswith(".wav")])
print(len(img_files), len(audio_files))
# 检查是否一一对应
assert len(img_files) == len(audio_files), "图像与音频数量不一致！"
assert all(os.path.splitext(f1)[0] == os.path.splitext(f2)[0] for f1, f2 in zip(img_files, audio_files)), "图像和音频文件名不匹配！"

# 写入 input.txt
with open(output_txt, "w") as f:
    for img_file, audio_file in zip(img_files, audio_files):
        name = os.path.splitext(img_file)[0]
        img_path = os.path.join(img_dir, img_file)
        audio_path = os.path.join(audio_dir, audio_file)
        line = f"a person is talking@@{img_path}@@{audio_path}\n"
        f.write(line)

print(f"✅ 已生成 {len(img_files)} 行 input.txt 到 {output_txt}")
