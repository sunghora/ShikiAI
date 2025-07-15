# LE_delete_dir.py フォルダ除去処理（再帰対応）

import shutil
from pathlib import Path

# === ShikiAI直下をルートとしてパス定義 ===
shiki_root = Path(__file__).resolve().parent.parent
src_dir = shiki_root / "preprocess" / "label_editor"
dst_dir = shiki_root / "preprocess" / "label_editor_output"

# 出力先がなければ作成
dst_dir.mkdir(parents=True, exist_ok=True)

if not src_dir.exists():
    raise FileNotFoundError(f"label_editorフォルダが存在しません: {src_dir}")

# === 再帰的にすべてのファイルを取得して移動 ===
for file in src_dir.rglob("*"):
    if file.is_file():
        dest = dst_dir / file.name
        if dest.exists():
            print(f"[スキップ] {file.name} は既に存在します。上書きしません。")
            continue

        shutil.move(str(file), str(dest))
        print(f"[移動] {file} → {dest}")

# === 空になったサブディレクトリを削除（深い階層から順に） ===
for folder in sorted(src_dir.rglob("*"), key=lambda p: -len(str(p))):
    if folder.is_dir():
        try:
            folder.rmdir()
            print(f"[削除] 空フォルダ: {folder}")
        except OSError:
            pass  # 中身があるフォルダは無視

print("✅ flatten 完了！全ファイルを移動し、空のフォルダを削除しました。")
