# LE_move_unpaired_images.py - 対応する.txtがない画像ファイルを移動

from pathlib import Path
import shutil

# === パス定義 ===
shiki_root = Path(__file__).resolve().parent.parent
src_dir = shiki_root / "preprocess" / "label_editor"
dst_dir = shiki_root / "preprocess" / "label_editor_missing_txt"

# === 出力先フォルダ作成 ===
dst_dir.mkdir(parents=True, exist_ok=True)

# === 対象画像拡張子 ===
image_exts = [".jpg", ".jpeg", ".png"]

# === 画像ファイルをチェック ===
for img_file in src_dir.glob("*"):
    if img_file.suffix.lower() not in image_exts:
        continue

    txt_file = img_file.with_suffix(".txt")
    if not txt_file.exists():
        # .txt が存在しない画像を移動
        dest = dst_dir / img_file.name
        shutil.move(str(img_file), str(dest))
        print(f"[移動] {img_file.name} → {dest.name}")

print("✅ .txt のない画像ファイルを label_editor_missing_txt に移動しました。")
