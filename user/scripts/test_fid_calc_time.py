import numpy as np
import torch
from scipy import linalg
import time
# new
import cupy as cp
import scipy
# from scipy.linalg import sqrtm
from torch_sqrtm import sqrtm, torch_matmul_to_array, np_to_gpu_tensor
from functools import partial

device = torch.device('cuda' if (torch.cuda.is_available()) else 'cpu')

# 2048 维度
d = 2048

# 随机生成 Inception 特征的均值和协方差
mu1 = np.random.randn(d)
mu2 = np.random.randn(d)
sigma1 = np.random.randn(d, d)
sigma1 = sigma1 @ sigma1.T  # 保证是正定矩阵
sigma2 = np.random.randn(d, d)
sigma2 = sigma2 @ sigma2.T  # 保证是正定矩阵

# 定义 Frechet Distance 计算函数
def calculate_frechet_distance(mu1, sigma1, mu2, sigma2, eps=1e-6):
    mu1 = np.atleast_1d(mu1)
    mu2 = np.atleast_1d(mu2)
    sigma1 = np.atleast_2d(sigma1)
    sigma2 = np.atleast_2d(sigma2)

    diff = mu1 - mu2
    start = time.time()
    covmean, _ = linalg.sqrtm(sigma1.dot(sigma2), disp=False)
    end = time.time()
    print(f"scipy.linalg.sqrtm 计算时间: {end - start:.4f} 秒")

    if not np.isfinite(covmean).all():
        offset = np.eye(sigma1.shape[0]) * eps
        covmean = linalg.sqrtm((sigma1 + offset).dot(sigma2 + offset))

    if np.iscomplexobj(covmean):
        covmean = covmean.real

    tr_covmean = np.trace(covmean)

    return (diff.dot(diff) + np.trace(sigma1) + np.trace(sigma2) - 2 * tr_covmean)


def calculate_frechet_distance_cpu2(mu_x: torch.Tensor, sigma_x: torch.Tensor, mu_y: torch.Tensor, sigma_y: torch.Tensor, device) -> torch.Tensor:
    mu_x = torch.from_numpy(mu_x).to(device)
    mu_y = torch.from_numpy(mu_y).to(device)
    sigma_x = torch.from_numpy(sigma_x).to(device)
    sigma_y = torch.from_numpy(sigma_y).to(device)

    a = (mu_x - mu_y).square().sum(dim=-1)
    b = sigma_x.trace() + sigma_y.trace()
    start = time.time()
    c = torch.linalg.eigvals(sigma_x @ sigma_y).sqrt().real.sum(dim=-1)
    end = time.time()
    print(f"torch.linalg 计算时间: {end - start:.4f} 秒")

    return a + b - 2 * c


def calculate_frechet_distance_gpu(mu1, sigma1, mu2, sigma2, device, eps=1e-6):

    array_to_tensor = partial(np_to_gpu_tensor, device)    
    mu1 = np.atleast_1d(mu1)
    mu2 = np.atleast_1d(mu2)

    sigma1 = np.atleast_2d(sigma1)
    sigma2 = np.atleast_2d(sigma2)

    assert mu1.shape == mu2.shape, \
        'Training and test mean vectors have different lengths'
    assert sigma1.shape == sigma2.shape, \
        'Training and test covariances have different dimensions'

    diff = mu1 - mu2

    # Product might be almost singular
    covmean, _ = sqrtm(torch_matmul_to_array(array_to_tensor(sigma1), array_to_tensor(sigma2)), array_to_tensor, disp=False)

    if not np.isfinite(covmean).all():
        msg = ('fid calculation produces singular product; '
            'adding %s to diagonal of cov estimates') % eps
        print(msg)
        offset = np.eye(sigma1.shape[0]) * eps
        covmean = sqrtm(torch_matmul_to_array(array_to_tensor(sigma1 + offset), array_to_tensor(sigma2 + offset)), array_to_tensor)

    # Numerical error might give slight imaginary component
    if np.iscomplexobj(covmean):
        if not np.allclose(np.diagonal(covmean).imag, 0, atol=1e-3):
            m = np.max(np.abs(covmean.imag))
            raise ValueError('Imaginary component {}'.format(m))
        covmean = covmean.real

    tr_covmean = np.trace(covmean)

    diff_ = array_to_tensor(diff)
    return (torch_matmul_to_array(diff_, diff_) + np.trace(sigma1) + np.trace(sigma2) - 2 * tr_covmean)


# 测试计算时间
start_time = time.time()
fid = calculate_frechet_distance_cpu2(mu1, sigma1, mu2, sigma2, device)
end_time = time.time()

print(f"Frechet Distance: {fid:.4f}")
print(f"⚡ 计算时间: {end_time - start_time:.4f} 秒")
