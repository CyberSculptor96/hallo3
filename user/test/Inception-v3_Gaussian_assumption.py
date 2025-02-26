import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os.path as osp

# 加载 Inception v3 模型（去掉分类头）
inception = models.inception_v3(pretrained=True, transform_input=False)
inception.fc = torch.nn.Identity()  # 移除分类层
inception.eval()

# 预处理图像的转换
transform = transforms.Compose([
    transforms.Resize((299, 299)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 加载示例图像
base_path = "/wangbenyou/huanghj/workspace/hallo3/user/test/imgs"
image_path = osp.join(base_path, "480_480.jpg")
image = Image.open(image_path).convert("RGB")
image = transform(image).unsqueeze(0)  # 添加 batch 维度

# 通过 Inception v3 计算 pool3 层特征
with torch.no_grad():
    features = inception(image)  # 提取特征

# 转换为 numpy 数组
features_np = features.squeeze().numpy()

# 绘制特征的直方图
plt.figure(figsize=(10, 5))
sns.histplot(features_np, bins=50, kde=True)
plt.title("Histogram of Inception-v3 Pool3 Layer Features")
plt.xlabel("Feature Value")
plt.ylabel("Frequency")
plt.grid(True)
# plt.show()
plt.savefig("histogram.png")

# Q-Q 图：检查特征分布是否接近高斯
plt.figure(figsize=(6, 6))
stats.probplot(features_np, dist="norm", plot=plt)
plt.title("Q-Q Plot of Inception-v3 Pool3 Layer Features")
plt.grid(True)
# plt.show()
plt.savefig("qq_plot.png")

# 计算 Shapiro-Wilk 正态性检验
shapiro_test = stats.shapiro(features_np[:500])  # 由于 Shapiro-Wilk 检验对大数据敏感，取前500个
print(shapiro_test)
