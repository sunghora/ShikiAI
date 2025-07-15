# LE_remove_duplicate_txt_pairs.py - 同じ画像とそのアノテーション削除＋残りを output に移動

from pathlib import Path
import hashlib
import shutil

# === パス設定 ===
shiki_root = Path(__file__).resolve().parent.parent
src_dir = shiki_root / "preprocess" / "label_editor"
dst_dir = shiki_root / "preprocess" / "label_editor_output"

dst_dir.mkdir(parents=True, exist_ok=True)

# === 画像の対応拡張子 ===
image_exts = [".jpg", ".jpeg", ".png"]

# === 重複.txtの検出用ハッシュマップ ===
hash_map = {}

for txt_file in src_dir.glob("*.txt"):
    with open(txt_file, "rb") as f:
        content = f.read()
        hash_val = hashlib.md5(content).hexdigest()
        hash_map.setdefault(hash_val, []).append(txt_file)

# === 重複アノテーションと対応画像の削除 ===
for hash_val, file_list in hash_map.items():
    if len(file_list) <= 1:
        continue  # 重複なし

    keep = file_list[0]
    to_delete = file_list[1:]

    print(f"[重複検出] {len(file_list)}件 → 残す: {keep.name}")

    for txt_path in to_delete:
        for ext in image_exts:
            img_path = txt_path.with_suffix(ext)
            if img_path.exists():
                img_path.unlink()
                print(f"  [削除] 画像: {img_path.name}")

        txt_path.unlink()
        print(f"  [削除] アノテーション: {txt_path.name}")

# === 残った画像＋.txtペアを output へ移動 ===
for txt_file in src_dir.glob("*.txt"):
    base = txt_file.stem

    # .txt を移動
    dst_txt = dst_dir / txt_file.name
    shutil.move(str(txt_file), str(dst_txt))
    print(f"[移動] {txt_file.name} → {dst_txt.name}")

    # 対応画像を探して移動
    for ext in image_exts:
        img_file = src_dir / f"{base}{ext}"
        if img_file.exists():
            dst_img = dst_dir / img_file.name
            shutil.move(str(img_file), str(dst_img))
            print(f"[移動] {img_file.name} → {dst_img.name}")

print("✅ 重複の削除と label_editor_output への移動が完了しました。")
