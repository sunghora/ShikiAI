# LE_merge.py
# merge_editor内にある二つのフォルダに対して、片方は未描写の画像のみ、片方は描写済みの
#画像とアノテーションがついているので、未描写＋アノテーションの構成にする

from pathlib import Path
import shutil

# === パス設定 ===
shiki_root = Path(__file__).resolve().parent.parent
base_dir = shiki_root / "preprocess" / "merge_editor"
src_img_dir = base_dir / "datasetA"
src_lbl_dir = base_dir / "datasetA_anno"
dst_dir = shiki_root / "preprocess" / "merge_editor_output"

dst_dir.mkdir(parents=True, exist_ok=True)

# === 対象拡張子 ===
image_exts = [".jpg", ".jpeg", ".png"]

merged_count = 0
missing_image = 0

# === アノテーションファイルを基準にマージ ===
for txt_file in src_lbl_dir.glob("*.txt"):
    base_name = txt_file.stem
    found_image = False

    for ext in image_exts:
        img_file = src_img_dir / f"{base_name}{ext}"
        if img_file.exists():
            # マージ実行
            shutil.copy2(img_file, dst_dir / img_file.name)
            shutil.copy2(txt_file, dst_dir / txt_file.name)
            merged_count += 1
            found_image = True
            print(f"[OK] {img_file.name} + {txt_file.name}")
            break

    if not found_image:
        print(f"[警告] {base_name}.* に対応する画像が datasetA に見つかりません")
        missing_image += 1

# === 結果 ===
print(f"\n✅ マージ完了！{merged_count} 件のペアを merge_editor_output に出力")
if missing_image:
    print(f"⚠️ 対応画像が見つからなかった .txt：{missing_image} 件")
