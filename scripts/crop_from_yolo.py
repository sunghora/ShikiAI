# crop_from_yolo.py
from pathlib import Path
import cv2
import csv

# === 設定 ===
input_dir = Path("annotations/datasetA")  # 画像とtxtが一緒の場所
output_dir = Path("crops")                # crop画像の出力先
mapping_path = output_dir / "mapping.csv" # cropと元画像の対応表

# 出力先を作成
output_dir.mkdir(parents=True, exist_ok=True)

# 拡張子定義
valid_exts = [".jpg", ".jpeg", ".png"]

# 対応表CSV書き出し用
mapping = []

# 処理開始
for img_path in input_dir.glob("*"):
    if img_path.suffix.lower() not in valid_exts:
        continue

    label_path = img_path.with_suffix(".txt")
    if not label_path.exists():
        continue

    img = cv2.imread(str(img_path))
    if img is None:
        print(f"[読み込み失敗] {img_path}")
        continue

    h_img, w_img = img.shape[:2]

    with open(label_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        parts = line.strip().split()
        if len(parts) != 5:
            continue  # YOLO形式でない行はスキップ

        class_id, x, y, w, h = map(float, parts)

        # YOLO → pixel座標に変換
        cx, cy = x * w_img, y * h_img
        bw, bh = w * w_img, h * h_img
        x1 = int(max(cx - bw / 2, 0))
        y1 = int(max(cy - bh / 2, 0))
        x2 = int(min(cx + bw / 2, w_img))
        y2 = int(min(cy + bh / 2, h_img))

        crop = img[y1:y2, x1:x2]
        crop_filename = f"{img_path.stem}_bbox{i}.jpg"
        crop_path = output_dir / crop_filename
        cv2.imwrite(str(crop_path), crop)

        mapping.append([img_path.name, label_path.name, crop_filename, class_id, i])

print(f"[完了] 作成crop数: {len(mapping)}")

# 対応表CSVを保存
with open(mapping_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["元画像", "YOLOラベル", "cropファイル名", "クラスID", "bbox番号"])
    writer.writerows(mapping)

print(f"[対応表出力] {mapping_path}")
