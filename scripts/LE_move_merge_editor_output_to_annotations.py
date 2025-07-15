# LE_move_merge_editor_output_to_annotations.py
# merge_editor_output のファイル群を任意のフォルダ名で annotations/ 以下に移動

from pathlib import Path
import shutil

# === 設定 ===
shiki_root = Path(__file__).resolve().parent.parent
src_dir = shiki_root / "preprocess" / "merge_editor_output"
annotations_dir = shiki_root / "annotations"

# === 任意の出力フォルダ名（★ここを変更！）===
target_name = "merged_dataset_v1"  # ← 好きなフォルダ名に変更してください

dst_dir = annotations_dir / target_name
dst_dir.mkdir(parents=True, exist_ok=True)

# === 対象ファイルをすべて移動 ===
count = 0
for file in src_dir.glob("*"):
    if file.is_file():
        dest = dst_dir / file.name
        if dest.exists():
            print(f"[スキップ] {file.name} は既に存在します")
        else:
            shutil.move(str(file), str(dest))
            print(f"[移動] {file.name} → {target_name}/")
            count += 1

print(f"\n✅ 移動完了：{count} 件のファイルを annotations/{target_name} に移動しました。")
