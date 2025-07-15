# LE_move_to_LE_from_split_80_20.py　split_80_20からlabel_editorへファイル移動

import shutil
from pathlib import Path

# === ディレクトリ定義 ===
shiki_root = Path(__file__).resolve().parent.parent
src_dir = shiki_root / "preprocess" / "split_80_20"
dst_dir = shiki_root / "preprocess" / "label_editor"

# 出力先ディレクトリが存在しなければ作成
dst_dir.mkdir(parents=True, exist_ok=True)

# === ファイル処理 ===
def generate_unique_name(base_name: str, extension: str, existing: set) -> str:
    """重複がある場合、アンダーバーを付けて回避するファイル名を生成"""
    candidate = f"{base_name}{extension}"
    while candidate in existing:
        base_name += "_1"
        candidate = f"{base_name}{extension}"
    return candidate

existing_files = {f.name for f in dst_dir.iterdir() if f.is_file()}

moved_count = 0

for item in src_dir.iterdir():
    if not item.is_file():
        continue

    stem = item.stem
    suffix = item.suffix.lower()

    # 新しいファイル名を "LE_" プレフィックス付きで構成
    base_name = f"LE_{stem}"
    new_name = generate_unique_name(base_name, suffix, existing_files)
    dest_path = dst_dir / new_name

    shutil.move(str(item), str(dest_path))
    existing_files.add(dest_path.name)
    moved_count += 1

    print(f"[移動] {item.name} → {dest_path.name}")

print(f"\n完了：{moved_count} 件のファイルを split_80_20 に移動しました。")
