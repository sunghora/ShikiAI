# yolo_draw_results_submit.py
# 提出用のBBox描画と黄色ナンバー判定スクリプト（すべて緑で描画）

from pathlib import Path
from ultralytics import YOLO
import cv2
import numpy as np
import os

# === ディレクトリ定義 ===
script_dir = Path(__file__).resolve().parent
shiki_root = script_dir.parent

model_path = shiki_root / "runs" / "detect_submit" / "weights" / "best.pt"
input_dir = shiki_root / "samples-confidential"
output_root = shiki_root / "results"

# モデルフォルダ名
folder_name = model_path.parents[1].name
parent_folder_name = folder_name.replace("detect_", "")
output_dir = output_root / f"outputs_{parent_folder_name}"
output_dir.mkdir(parents=True, exist_ok=True)

print(f"[INFO] モデル: {model_path}")
print(f"[INFO] 入力画像フォルダ: {input_dir}")
print(f"[INFO] 出力フォルダ: {output_dir}")

# === 黄色判定パラメータ ===
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])
yellow_pixel_threshold = 50

# === モデル読み込み ===
model = YOLO(str(model_path))

# 対象拡張子
valid_exts = [".jpg", ".jpeg", ".png", ".bmp"]
yellow_plate_total = 0

# === 処理ループ ===
for img_name in os.listdir(input_dir):
    if not any(img_name.lower().endswith(ext) for ext in valid_exts):
        continue

    img_path = input_dir / img_name
    img = cv2.imread(str(img_path))
    if img is None:
        print(f"[ERROR] 読み込み失敗: {img_path}")
        continue

    results = model(img)
    boxes = results[0].boxes

    yellow_plate_count = 0
    h, w = img.shape[:2]
    used_boxes = []

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy.tolist()[0])
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w - 1, x2), min(h - 1, y2)

        # 重複チェック（IOU）
        overlap = False
        for ux1, uy1, ux2, uy2 in used_boxes:
            iou_area = max(0, min(x2, ux2) - max(x1, ux1)) * max(0, min(y2, uy2) - max(y1, uy1))
            if iou_area > 0:
                overlap = True
                break
        if overlap:
            continue
        used_boxes.append((x1, y1, x2, y2))

        roi = img[y1:y2, x1:x2]
        if roi.size == 0:
            continue

        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, lower_yellow, upper_yellow)
        yellow_pixels = cv2.countNonZero(mask)

        if yellow_pixels > yellow_pixel_threshold:
            yellow_plate_count += 1

        # 黄色ナンバー含め、すべて緑で囲む
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    yellow_plate_total += yellow_plate_count
    print(f"{img_name}: Yellow Plates detected = {yellow_plate_count}")
    save_path = output_dir / img_name
    cv2.imwrite(str(save_path), img)

# === 検出数ログ出力 ===
summary_txt = output_dir / "黄色ナンバー数.txt"
with summary_txt.open("w", encoding="utf-8") as f:
    f.write(f"黄色ナンバー数: {yellow_plate_total}\n")

print("\n✅ 全画像の処理が完了しました。")
print(f"🟨 総黄色ナンバー数: {yellow_plate_total}")
print(f"[出力] {summary_txt}")
