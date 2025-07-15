# yolo_results.py  メイン処理。学習済みモデルから画像認識させ、OpenCVを用いて描写処理、黄色ナンバー計測を行う

from pathlib import Path
from ultralytics import YOLO
import cv2
import numpy as np
import os

# === ディレクトリ定義 ===
script_dir = Path(__file__).resolve().parent
shiki_root = script_dir.parent

model_path = shiki_root / "runs" / "detect_exp27" / "weights" / "best.pt"
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

# === クラス定義 ===
CLASS_CLEAR = 0         # clear_plate（緑）
CLASS_PARTIAL = 1       # partial_plate（青）

class_colors = {
    CLASS_CLEAR: ((0, 255, 0), "clear_plate"),      # 緑
    CLASS_PARTIAL: ((255, 0, 0), "partial_plate")   # 青
}

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

    for box in boxes:
        cls_id = int(box.cls[0])
        if cls_id not in class_colors:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy.tolist()[0])
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w - 1, x2), min(h - 1, y2)

        roi = img[y1:y2, x1:x2]
        if roi.size == 0:
            continue

        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, lower_yellow, upper_yellow)
        yellow_pixels = cv2.countNonZero(mask)

        color, label = class_colors[cls_id]
        label_draw = label

        if yellow_pixels > yellow_pixel_threshold:
            color = (0, 255, 255)  # 黄色
            label_draw = "Yellow Plate"
            yellow_plate_count += 1

        text_y = max(y1 - 10, 10)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, label_draw, (x1, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

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
