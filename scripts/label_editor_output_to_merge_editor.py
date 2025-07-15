# label_editor_output_to_merge_editor.py
# label_editor_output → merge_editor/datasetA_anno にペアファイルをコピー

from pathlib import Path
import shutil

# === パス定義 ===
shiki_root = Path(__file__).resolve().parent.parent
src_dir = shiki_root / "preprocess" / "label_editor_output"
dst_base = shiki_root / "preprocess" / "merge_editor" / "datasetA_anno"

# 出力先ディレクトリを作成（存在すればスキップ）
dst_base.mkdir(parents=True, exist_ok=True)

# 対象拡張子
image_exts = [".jpg", ".jpeg", ".png"]

# === 処理開始 ===
count = 0
for image_file in src_dir.iterdir():
    if image_file.suffix.lower() not in image_exts:
        continue

    txt_file = image_file.with_suffix(".txt")
    if not txt_file.exists():
        print(f"[スキップ] {image_file.name} に対応する .txt が見つかりません")
        continue

    # 画像と .txt をコピー
    shutil.copy2(image_file, dst_base / image_file.name)
    shutil.copy2(txt_file, dst_base / txt_file.name)
    count += 1
    print(f"[コピー] {image_file.name} + {txt_file.name}")

print(f"\n✅ コピー完了！ペア数: {count} 件")
print(f"📂 保存先: {dst_base}")
