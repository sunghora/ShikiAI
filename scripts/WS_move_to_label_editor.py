# WS_move_to_label_editor.py workspace/move_to_label_editorからlabel_editorへ移行処理

import shutil
from pathlib import Path

# === ShikiAI直下をルートとして明示 ===
shiki_root = Path(__file__).resolve().parent.parent  # scripts/ の1つ上 → ShikiAI/
src_dir = shiki_root / "workspace" / "move_to_label_editor"
dst_dir = shiki_root / "preprocess" / "label_editor"

# フォルダ存在確認
if not src_dir.exists():
    raise FileNotFoundError(f"移行元フォルダが存在しません: {src_dir}")

if not dst_dir.exists():
    dst_dir.mkdir(parents=True)
    print(f"移行先フォルダを作成しました: {dst_dir}")

# ファイルとフォルダの移動処理
for item in src_dir.iterdir():
    dest_path = dst_dir / item.name
    print(f"[移動中] {item} → {dest_path}")
    shutil.move(str(item), str(dest_path))

print("移動完了！")
