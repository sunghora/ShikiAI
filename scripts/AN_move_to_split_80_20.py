# AN_move_to_split_80_20.py
# split_input から split_80_20 へファイル移動（フォルダ含む）

import shutil
from pathlib import Path

# === ディレクトリ定義 ===
shiki_root = Path(__file__).resolve().parent.parent
src_dir = shiki_root / "annotations" / "split_input"
dst_dir = shiki_root / "preprocess" / "split_80_20"

# 出力先ディレクトリが存在しなければ作成
dst_dir.mkdir(parents=True, exist_ok=True)

# === ユニークファイル名生成関数 ===
def generate_unique_name(base_name: str, extension: str, existing: set) -> str:
    candidate = f"{base_name}{extension}"
    while candidate in existing:
        base_name += "_1"
        candidate = f"{base_name}{extension}"
    return candidate

# === 既存ファイル名を把握 ===
existing_files = {f.name for f in dst_dir.iterdir() if f.is_file()}
moved_count = 0

# === split_input 内を走査（ファイル・フォルダ両方） ===
for item in src_dir.iterdir():
    if item.is_file():
        items_to_process = [item]
        parent_desc = ""
    elif item.is_dir():
        items_to_process = list(item.rglob("*"))  # 再帰的にファイル取得
        parent_desc = f"[フォルダ: {item.name}] "
    else:
        continue

    for file in items_to_process:
        if not file.is_file():
            continue

        stem = file.stem
        suffix = file.suffix.lower()

        base_name = f"{stem}"
        new_name = generate_unique_name(base_name, suffix, existing_files)
        dest_path = dst_dir / new_name

        shutil.move(str(file), str(dest_path))
        existing_files.add(dest_path.name)
        moved_count += 1

        print(f"{parent_desc}[移動] {file.name} → {dest_path.name}")

    # --- フォルダだった場合、移動完了後に削除 ---
    if item.is_dir():
        try:
            item.rmdir()
            print(f"[削除] 空フォルダ削除: {item.name}")
        except OSError as e:
            print(f"[警告] フォルダ未削除（空でない）: {item.name} → {e}")

print(f"\n✅ 完了：{moved_count} 件のファイルを split_80_20 に移動しました。")
