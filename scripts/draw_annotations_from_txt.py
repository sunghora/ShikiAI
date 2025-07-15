# draw_annotations_from_txt.py
# YOLO形式アノテーション(.txt)を画像に描写し、出力フォルダに保存
# labelimgで読み込まなくとも、アノテーション制度を確認できるようのフォルダ生成コマンド

import cv2
from pathlib import Path

# === パス定義 ===
shiki_root = Path(__file__).resolve().parent.parent
input_dir = shiki_root / "annotations" / "merged_dataset_v1"
output_dir = shiki_root / "annotated_output" / "merged_dataset_v1"
output_dir.mkdir(parents=True, exist_ok=True)

# === クラス色（任意：最大5クラス分） ===
colors = [
    (0, 255, 0),     # class 0: green
    (0, 0, 255),     # class 1: red
    (255, 255, 0),   # class 2: cyan
    (255, 0, 255),   # class 3: magenta
    (0, 255, 255),   # class 4: yellow
]

# === 処理開始 ===
image_exts = [".jpg", ".jpeg", ".png"]
count = 0

for image_file in input_dir.iterdir():
    if image_file.suffix.lower() not in image_exts:
        continue

    txt_file = image_file.with_suffix(".txt")
    if not txt_file.exists():
        print(f"[スキップ] {image_file.name} に対応する .txt が見つかりません")
        continue

    img = cv2.imread(str(image_file))
    if img is None:
        print(f"[読み込み失敗] {image_file.name}")
        continue

    h, w = img.shape[:2]

    # アノテーション読み取り
    with open(txt_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            continue
        class_id, x_center, y_center, box_w, box_h = map(float, parts)
        class_id = int(class_id)

        # YOLO → pixel 座標変換
        xc = int(x_center * w)
        yc = int(y_center * h)
        bw = int(box_w * w)
        bh = int(box_h * h)
        x1 = int(xc - bw / 2)
        y1 = int(yc - bh / 2)
        x2 = int(xc + bw / 2)
        y2 = int(yc + bh / 2)

        color = colors[class_id % len(colors)]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, f"Class {class_id}", (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1, cv2.LINE_AA)

    # 出力保存
    out_path = output_dir / image_file.name
    cv2.imwrite(str(out_path), img)
    count += 1
    print(f"[保存] {out_path.name}")

print(f"\n✅ 描写完了！合計 {count} 枚の画像にバウンディングボックスを描写しました。")
print(f"📂 出力先：{output_dir.resolve()}")
