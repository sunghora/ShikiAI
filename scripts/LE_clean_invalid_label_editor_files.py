# LE_clean_invalid_label_editor_files.py ペアが不正なファイルを削除

from pathlib import Path

# === 対象ディレクトリ ===
shiki_root = Path(__file__).resolve().parent.parent
check_dir = shiki_root / "preprocess" / "label_editor"

# === 拡張子定義 ===
image_exts = {".jpg", ".jpeg", ".png"}

# === ベース名収集 ===
image_stems = {}
txt_stems = {}

for file in check_dir.iterdir():
    if not file.is_file():
        continue
    suffix = file.suffix.lower()
    stem = file.stem
    if suffix in image_exts:
        image_stems[stem] = file
    elif suffix == ".txt":
        txt_stems[stem] = file

# 不正なファイル検出（片方しか存在しないもの）
invalid_files = []

for stem, file in image_stems.items():
    if stem not in txt_stems:
        invalid_files.append(file)

for stem, file in txt_stems.items():
    if stem not in image_stems:
        invalid_files.append(file)

# === 削除処理 ===
print("=== 不正ファイル削除 ===")
if not invalid_files:
    print("✅ 不正ファイルは見つかりませんでした。")
else:
    for f in invalid_files:
        print(f"[削除] {f.name}")
        f.unlink()  # ファイル削除

    print(f"\n✅ 削除完了：{len(invalid_files)} 件")

