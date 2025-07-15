# LE_check_label_editor_pairs.py label_editorに格納されている画像とtxtファイルのペアに問題がないか確認

from pathlib import Path

# === 対象ディレクトリ ===
shiki_root = Path(__file__).resolve().parent.parent
check_dir = shiki_root / "preprocess" / "label_editor"

# === 拡張子設定 ===
image_exts = {".jpg", ".jpeg", ".png"}

# === ベース名抽出 ===
image_stems = set()
txt_stems = set()
all_invalid = []

for file in check_dir.iterdir():
    if not file.is_file():
        continue

    suffix = file.suffix.lower()
    stem = file.stem

    if suffix in image_exts:
        image_stems.add(stem)
    elif suffix == ".txt":
        txt_stems.add(stem)

# 画像だけある or txtだけあるもの
only_img = image_stems - txt_stems
only_txt = txt_stems - image_stems

# 不正ファイル名リストにまとめる
for stem in sorted(only_img):
    all_invalid.append(f"{stem}{Path('.jpg')}")
for stem in sorted(only_txt):
    all_invalid.append(f"{stem}.txt")

# === 結果出力 ===
print("=== チェック結果 ===")
if not all_invalid:
    print("✅ すべてのファイルは正しいペアになっています。")
else:
    print(f"❌ 不正ファイル数: {len(all_invalid)} 件")
    for name in all_invalid:
        print(f" - {name}")

