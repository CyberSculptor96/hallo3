import json
import os

# 输入文件路径
input_file = '/wangbenyou/huanghj/workspace/hallo3/json/data_sampled_filtered.json'
# 输出文件路径
output_file = '/wangbenyou/huanghj/workspace/hallo3/json/data_sampled_filtered_filtered.json'
# 输出文件夹目录路径
output_folder = '/wangbenyou/huanghj/workspace/hallo3/output/output_testset'

# 获取 output_testset 目录下所有文件夹名，并提取出每个文件夹的 id 部分（去除 "-seed" 后缀）
output_folders = os.listdir(output_folder)
valid_folders = {folder.split('-seed')[0] for folder in output_folders}  # 使用集合去重
print(f"{len(valid_folders)=}")
print(valid_folders)
# 读取原始 JSON 文件
with open(input_file, 'r') as f:
    data = json.load(f)

# 筛选出那些 id 字段的值对应文件夹名存在于 output_testset 目录中的数据
filtered_data = []
for item in data:
    video_id = item.get("id")
    # 提取 id 字段中对应的视频文件夹名部分，去除 'videovideo' 前缀
    folder_name = video_id[10:]
    folder_name = folder_name.rsplit('-', 1)
    folder_name = '_'.join(folder_name)
    # print(folder_name)
    if folder_name in valid_folders:
        filtered_data.append(item)

# 将筛选后的数据写入新的 JSON 文件
with open(output_file, 'w') as f:
    json.dump(filtered_data, f, indent=4)

print(f"新文件已保存到: {output_file}")

# 提取所有 JSON 中的 id 字段
json_ids = [item.get("id") for item in data]

# 检查 valid_folders 中的每个文件夹是否能在 JSON 中找到对应的 id
missing_folders = []
for folder in valid_folders:
    # 生成对应的 video_id（去掉前缀，并将最后一个 - 替换为 _）
    video_id = 'videovideo' + folder.rsplit('_', 1)[0] + '-' + folder.rsplit('_', 1)[1]
    
    # 检查 video_id 是否在 JSON 的 id 列表中
    if video_id not in json_ids:
        missing_folders.append(video_id)

# 输出未找到的文件夹
if missing_folders:
    print("以下文件夹未能在 JSON 中找到对应的 id:")
    # for folder in missing_folders:
    #     print(folder)
    print(len(missing_folders))
else:
    print("所有文件夹都能在 JSON 中找到对应的数据。")