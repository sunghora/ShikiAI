# LE_clear_merge_editor.py
# merge_editor_ フォルダ内の全ファイルを削除

from pathlib import Path

# === パス定義 ===
shiki_root = Path(__file__).resolve().parent.parent
target_dir = shiki_root / "preprocess" / "merge_editor"

if not target_dir.exists():
    raise FileNotFoundError(f"[エラー] フォルダが存在しません: {target_dir}")

count = 0
for file in target_dir.iterdir():
    if file.is_file():
        file.unlink()
        print(f"[削除] {file.name}")
        count += 1

print(f"\n✅ 削除完了！合計 {count} 件のファイルを削除しました。")
