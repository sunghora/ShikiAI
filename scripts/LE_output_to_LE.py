# LE_move_to_only_train.py　label_editor から images/train, labels/train へファイル移動

import shutil
from pathlib import Path

# === ディレクトリ定義 ===
shiki_root = Path(__file__).resolve().parent.parent
src_dir = shiki_root / "preprocess" / "label_editor"

images_train_dir = shiki_root / "images" / "train"
labels_train_dir = shiki_root / "labels" / "train"

# 出力先ディレクトリが存在しなければ作成
images_train_dir.mkdir(parents=True, exist_ok=True)
labels_train_dir.mkdir(parents=True, exist_ok=True)

# === ファイル処理 ===
def generate_unique_name(base_name: str, extension: str, existing: set) -> str:
    """重複がある場合、アンダーバーを付けて回避するファイル名を生成"""
    candidate = f"{base_name}{extension}"
    while candidate in existing:
        base_name += "_1"
        candidate = f"{base_name}{extension}"
    return candidate

existing_images = {f.name for f in images_train_dir.iterdir() if f.is_file()}
existing_labels = {f.name for f in labels_train_dir.iterdir() if f.is_file()}

moved_count = 0

for item in src_dir.iterdir():
    if not item.is_file():
        continue

    stem = item.stem
    suffix = item.suffix.lower()

    base_name = f"LE_{stem}"

    if suffix in [".jpg", ".jpeg", ".png"]:
        new_name = generate_unique_name(base_name, suffix, existing_images)
        dest_path = images_train_dir / new_name
        existing_images.add(new_name)
    elif suffix == ".txt":
        new_name = generate_unique_name(base_name, suffix, existing_labels)
        dest_path = labels_train_dir / new_name
        existing_labels.add(new_name)
    else:
        continue  # 対象外ファイルはスキップ

    shutil.move(str(item), str(dest_path))
    moved_count += 1
    print(f"[移動] {item.name} → {dest_path.name}")

print(f"\n✅ 完了：{moved_count} 件のファイルを images/train または labels/train に移動しました。")
