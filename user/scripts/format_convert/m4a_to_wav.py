import os
import subprocess
from tqdm import tqdm
# 设置输入目录
input_dir = "/wangbenyou/huanghj/workspace/hallo3/examples/test_data-0331/audios"
output_dir = "/wangbenyou/huanghj/workspace/hallo3/examples/test_data-0331/audio"

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 遍历目录中的 .m4a 文件
for file_name in tqdm(os.listdir(input_dir)):
    if file_name.endswith(".m4a"):
        input_file = os.path.join(input_dir, file_name)
        output_file = os.path.join(output_dir, file_name.replace(".m4a", ".wav"))
        
        # 执行 ffmpeg 命令
        command = ["ffmpeg", "-i", input_file, "-v", "error", "-acodec", "pcm_s16le", "-ar", "16000", output_file]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print("All conversions completed.")