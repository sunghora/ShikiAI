# split_image_label_to_train.py

import shutil
from pathlib import Path

# === 設定 ===
shiki_root = Path(__file__).resolve().parent.parent
src_dir = shiki_root / "preprocess" / "split_80_20"

images_train_dir = shiki_root / "images" / "train"
labels_train_dir = shiki_root / "labels" / "train"

# 画像拡張子対象
image_exts = {".jpg", ".jpeg", ".png"}

# 出力先ディレクトリを作成（なければ作る）
images_train_dir.mkdir(parents=True, exist_ok=True)
labels_train_dir.mkdir(parents=True, exist_ok=True)

# === ペア収集＆移動 ===
moved_count = 0
for img_path in src_dir.iterdir():
    if not img_path.is_file():
        continue
    if img_path.suffix.lower() not in image_exts:
        continue

    txt_path = src_dir / (img_path.stem + ".txt")
    if not txt_path.exists():
        print(f"[警告] 対応する .txt が見つかりません: {img_path.name}")
        continue

    # 画像移動
    shutil.move(str(img_path), str(images_train_dir / img_path.name))
    # ラベル移動
    shutil.move(str(txt_path), str(labels_train_dir / txt_path.name))

    print(f"[移動] {img_path.name} / {txt_path.name}")
    moved_count += 1

print(f"\n完了！移動ペア数: {moved_count} 件")
