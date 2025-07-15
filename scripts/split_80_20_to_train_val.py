# split_80_20_to_train_val.py

import shutil
import random
from pathlib import Path

# === 設定 ===
shiki_root = Path(__file__).resolve().parent.parent
src_dir = shiki_root / "preprocess" / "split_80_20"

images_train_dir = shiki_root / "images" / "train"
images_val_dir   = shiki_root / "images" / "val"
labels_train_dir = shiki_root / "labels" / "train"
labels_val_dir   = shiki_root / "labels" / "val"

# 画像拡張子対象
image_exts = {".jpg", ".jpeg", ".png"}

# 出力先ディレクトリを作成
for d in [images_train_dir, images_val_dir, labels_train_dir, labels_val_dir]:
    d.mkdir(parents=True, exist_ok=True)

# === ペア収集 ===
pairs = []
for img_path in src_dir.iterdir():
    if not img_path.is_file():
        continue
    if img_path.suffix.lower() not in image_exts:
        continue

    txt_path = src_dir / (img_path.stem + ".txt")
    if not txt_path.exists():
        print(f"[警告] 対応する .txt が見つかりません: {img_path.name}")
        continue

    pairs.append((img_path, txt_path))

print(f"総ペア数: {len(pairs)}")

# === ランダムシャッフルして8:2に分割 ===
random.shuffle(pairs)
split_index = int(len(pairs) * 0.8)
train_pairs = pairs[:split_index]
val_pairs   = pairs[split_index:]

# === 移動関数 ===
def move_pair(img_path, txt_path, img_dst_dir, txt_dst_dir):
    shutil.move(str(img_path), str(img_dst_dir / img_path.name))
    shutil.move(str(txt_path), str(txt_dst_dir / txt_path.name))
    print(f"[移動] {img_path.name} / {txt_path.name}")

# === 移動処理 ===
print("\n[TRAINへ移動]")
for img, txt in train_pairs:
    move_pair(img, txt, images_train_dir, labels_train_dir)

print("\n[VALへ移動]")
for img, txt in val_pairs:
    move_pair(img, txt, images_val_dir, labels_val_dir)

print(f"\n完了！Train: {len(train_pairs)} 件, Val: {len(val_pairs)} 件")
