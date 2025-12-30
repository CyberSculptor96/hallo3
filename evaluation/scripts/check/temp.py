import pandas as pd
from pathlib import Path

# 输入路径
csv_path = Path("/wangbenyou/huanghj/workspace/hallo3/evaluation/vico_challenge_baseline/csv/annotations-176.csv")
missing_path = Path("/wangbenyou/huanghj/workspace/hallo3/evaluation/dataset/scripts/check/missing_gen_files.txt")
output_path = csv_path.parent / "annotations-164.csv"

# 1. 读取 annotation CSV
df = pd.read_csv(csv_path)

# 2. 读取缺失文件名列表
with open(missing_path, "r") as f:
    missing_files = set(line.strip() for line in f if line.strip())

# 3. 过滤掉包含缺失文件的行（检查 gt 或 pd 任一列）
filtered_df = df[~(df['gt_filename'].isin(missing_files) | df['pd_filename'].isin(missing_files))]

# 4. 保存为新 CSV
filtered_df.to_csv(output_path, index=False)

print(f"✅ 原始数据行数: {len(df)}")
print(f"❌ 被移除的行数: {len(df) - len(filtered_df)}")
print(f"📄 已保存至: {output_path}")
