# LE_rename_pairs.py 画像ファイルとそのペアtxtの名前をシンプルにする（1.jpg 1.txt 2.jpg 2.txt等）

import shutil
from pathlib import Path

# ルート設定
shiki_root = Path(__file__).resolve().parent.parent
src_dir = shiki_root / "preprocess" / "label_editor"
dst_dir = shiki_root / "preprocess" / "label_editor_output"

# 出力先がなければ作成
dst_dir.mkdir(parents=True, exist_ok=True)

# 拡張子ごとにファイルを収集
jpg_files = {f.stem: f for f in src_dir.glob("*.jpg")}
txt_files = {f.stem: f for f in src_dir.glob("*.txt")}

# ペアを取得（ベース名が一致するもの）
common_stems = sorted(set(jpg_files.keys()) & set(txt_files.keys()))
print(f"検出されたペア数: {len(common_stems)}")

# ペアごとにリネーム移動
for idx, stem in enumerate(common_stems, start=1):
    jpg_src = jpg_files[stem]
    txt_src = txt_files[stem]

    jpg_dst = dst_dir / f"{idx}.jpg"
    txt_dst = dst_dir / f"{idx}.txt"

    if jpg_dst.exists() or txt_dst.exists():
        print(f"[スキップ] {jpg_dst.name} または {txt_dst.name} が既に存在します")
        continue

    shutil.move(str(jpg_src), str(jpg_dst))
    shutil.move(str(txt_src), str(txt_dst))
    print(f"[移動＆リネーム] {stem}.jpg/.txt → {idx}.jpg/.txt")

print("\nすべてのペアの処理が完了しました！")
