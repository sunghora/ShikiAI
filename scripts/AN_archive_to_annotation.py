# AN_archive_to_annotation.py imagesとlabels配下の学習セットをarchives/へ移行

import shutil
from pathlib import Path

# === ルート定義 ===
shiki_root = Path(__file__).resolve().parent.parent
images_dir = shiki_root / "images"
labels_dir = shiki_root / "labels"
anno_case_root = shiki_root / "annotations" / "archives"

# === case_x フォルダ名決定 ===
i = 1
while True:
    case_dir = anno_case_root / f"case_{i}"
    if not case_dir.exists():
        break
    i += 1

case_dir.mkdir(parents=True)
print(f"[作成] 保存先フォルダ: {case_dir}")

# === 対象拡張子 ===
image_exts = {".jpg", ".jpeg", ".png"}
pair_count = 0

# === train/val 内のファイルを移動 ===
for subdir in ["train", "val"]:
    for img_file in (images_dir / subdir).glob("*"):
        if img_file.suffix.lower() in image_exts:
            txt_file = labels_dir / subdir / (img_file.stem + ".txt")
            if txt_file.exists():
                # 両方ある場合 → move してカウント
                shutil.move(str(img_file), str(case_dir / img_file.name))
                shutil.move(str(txt_file), str(case_dir / txt_file.name))
                print(f"[移動] {img_file.name} / {txt_file.name}")
                pair_count += 1
            else:
                print(f"[警告] {img_file.name} に対応する .txt が見つかりません。スキップ。")
        else:
            print(f"[スキップ] 非画像ファイル: {img_file.name}")

# === 件数ファイルの出力 ===
count_file = case_dir / "ファイル数.txt"
with count_file.open("w", encoding="utf-8") as f:
    f.write(f"{pair_count}\n")

print(f"\n✅ 完了：{pair_count} 件のペアを {case_dir.name} に移動しました。")
print(f"[出力] {count_file.name} にペア数を記録しました。")
