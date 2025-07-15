# coding: utf-8
import shutil
from pathlib import Path

# === ルートパスの定義 ===
script_dir = Path(__file__).resolve().parent
shiki_root = script_dir.parent

# === 削除対象のディレクトリ ===
target_dirs = [
    shiki_root / "images" / "train",
    shiki_root / "images" / "val",
    shiki_root / "labels" / "train",
    shiki_root / "labels" / "val"
]

# === フォルダ削除処理 ===
for d in target_dirs:
    if d.exists() and d.is_dir():
        shutil.rmtree(d)
        print(f"[削除完了] {d}")
    else:
        print(f"[スキップ] {d} は存在しません")

# === キャッシュファイルも削除（あれば） ===
cache_files = [
    shiki_root / "labels" / "train.cache",
    shiki_root / "labels" / "val.cache"
]

for f in cache_files:
    if f.exists():
        f.unlink()
        print(f"[削除完了] {f}")
    else:
        print(f"[スキップ] {f} は存在しません")

print("✅ 指定フォルダの削除処理が完了しました。")
