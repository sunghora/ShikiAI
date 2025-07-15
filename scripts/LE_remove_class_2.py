# LE_remove_class_2.py

from pathlib import Path
import shutil

# === パス設定 ===
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent

input_dir = project_root / "preprocess" / "label_editor"
output_dir = project_root / "preprocess" / "label_editor_output"

output_dir.mkdir(parents=True, exist_ok=True)

# === 対象ファイル処理 ===
txt_files = list(input_dir.glob("*.txt"))
print(f"処理対象ファイル数: {len(txt_files)}\n")

for txt_path in txt_files:
    lines = txt_path.read_text(encoding="utf-8").splitlines()
    filtered = [line for line in lines if not line.strip().startswith("2 ")]

    removed_count = len(lines) - len(filtered)

    # 出力先パス
    out_txt_path = output_dir / txt_path.name
    out_txt_path.write_text("\n".join(filtered) + ("\n" if filtered else ""), encoding="utf-8")

    # 対応する画像（.jpg）の移動
    img_path = input_dir / (txt_path.stem + ".jpg")
    if img_path.exists():
        out_img_path = output_dir / img_path.name
        shutil.move(str(img_path), str(out_img_path))
        print(f"[OK] {txt_path.name} / {img_path.name} → 移動完了（削除: {removed_count} 行）")
    else:
        print(f"[警告] 対応画像なし: {txt_path.name}（削除: {removed_count} 行）")

    # 元の .txt は削除
    txt_path.unlink()

print("\n完了！")
