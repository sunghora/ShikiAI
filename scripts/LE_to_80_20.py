# LE_output_to_LE.py label_editorからsplit_80_20フォルダへ無処理移動

import shutil
from pathlib import Path
from collections import defaultdict

shiki_root = Path(__file__).resolve().parent.parent
src_dir = shiki_root / "preprocess" / "label_editor"
dst_dir = shiki_root / "preprocess" / "split_80_20"

if not src_dir.exists():
    raise FileNotFoundError(f"移行元フォルダが存在しません: {src_dir}")

dst_dir.mkdir(parents=True, exist_ok=True)

ext_counter = defaultdict(int)

for item in src_dir.iterdir():
    dest = dst_dir / item.name

    if dest.exists():
        print(f"[スキップ] {dest.name} は既に存在します。")
        continue

    # ★★★ 移動前に拡張子を取得するのがポイント ★★★
    if item.is_file():
        ext = item.suffix.lower() or "[no ext]"
    elif item.is_dir():
        ext = "DIR"
    else:
        ext = "OTHER"

    shutil.move(str(item), str(dest))
    print(f"[移動] {item.name} → {dest.name}")

    ext_counter[ext] += 1

# 出力
print("\n=== 移動件数（拡張子別） ===")
for ext, count in sorted(ext_counter.items()):
    print(f"{ext}: {count} 件")

print("\n移動処理 完了！")
