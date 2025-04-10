import os

# 设置路径
base_dir = "/wangbenyou/huanghj/workspace/hallo3/output/output_testset-0320/10k-steps"
output_txt_path = "/wangbenyou/huanghj/workspace/hallo3/output/output_sentences.txt"

# 原始句子模板
sentence_template = (
    "a person is talking@@"
    "/wangbenyou/huanghj/workspace/hallo3/examples/test_data-0320/imgs/{}_first_frame.png@@"
    "/wangbenyou/huanghj/workspace/hallo3/examples/test_data-0320/audios/{}_first_frame.wav"
)

# 获取所有子目录的名字
dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

# 生成句子并写入文件
with open(output_txt_path, 'w') as f:
    for dirname in dirs:
        sentence = sentence_template.format(dirname, dirname)
        f.write(sentence + "\n")

print(f"Generated {len(dirs)} sentences in {output_txt_path}.")
