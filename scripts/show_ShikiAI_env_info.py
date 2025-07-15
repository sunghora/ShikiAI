# ShikiAI_env環境下に導入されているパッケージ等のバージョンを取得しメモ帳に保存

# coding: utf-8

import torch
import torchvision
import numpy as np
import matplotlib
import subprocess
import ultralytics
import cv2
import PIL
from pathlib import Path

# 出力バッファ
output_lines = []

# === PyTorch / CUDA ===
output_lines.append("==== 機械学習・AIライブラリ ====")
output_lines.append(f"PyTorch=={torch.__version__}")
output_lines.append(f"torchvision=={torchvision.__version__}")
output_lines.append(f"CUDAランタイム=={torch.version.cuda}")
output_lines.append(f"cuDNN=={torch.backends.cudnn.version()}")
gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A"
output_lines.append(f"GPU=={gpu_name}")

# === CUDA Toolkit ===
output_lines.append("\n==== CUDA Toolkit（nvcc） ====")
try:
    nvcc_output = subprocess.check_output(["nvcc", "--version"], stderr=subprocess.STDOUT, text=True)
    last_line = nvcc_output.splitlines()[-1]
    output_lines.append(f"nvcc=={last_line}")
except FileNotFoundError:
    output_lines.append("nvcc not found: CUDA Toolkit not installed")
except subprocess.CalledProcessError as e:
    output_lines.append(f"nvcc error: {e.output.strip()}")

# === 物体検出・画像処理関連 ===
output_lines.append("\n==== 物体検出・画像処理関連 ====")
output_lines.append(f"ultralytics=={ultralytics.__version__}")
output_lines.append(f"YOLOv8=={ultralytics.__version__}")  # 同一
output_lines.append(f"OpenCV=={cv2.__version__}")
output_lines.append(f"Pillow=={PIL.__version__}")

# labelImg Gitバージョン確認
output_lines.append("\nlabelImg Version (from git):")
labelimg_path = Path("labelImg")
if labelimg_path.exists() and (labelimg_path / ".git").exists():
    try:
        result = subprocess.check_output(
            ["git", "-C", str(labelimg_path), "describe", "--tags", "--always"],
            stderr=subprocess.STDOUT,
            text=True
        )
        output_lines.append(f"labelImg=={result.strip()}")
    except subprocess.CalledProcessError as e:
        output_lines.append(f"Gitコマンド実行エラー: {e.output.strip()}")
else:
    output_lines.append("labelImg ディレクトリが見つからないか .git が存在しません")

# === 検証・可視化・解析 ===
output_lines.append("\n==== 検証・可視化・解析 ====")
output_lines.append(f"NumPy=={np.__version__}")
output_lines.append(f"matplotlib=={matplotlib.__version__}")

# === 出力処理 ===
requirements_path = Path("env_versions_report.txt")
with open(requirements_path, "w", encoding="utf-8") as f:
    for line in output_lines:
        print(line)       # コンソール出力
        f.write(line + "\n")

print(f"\n✅ 出力完了: {requirements_path.resolve()}")
