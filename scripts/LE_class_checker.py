# LE_class_checker.py

from pathlib import Path
from collections import Counter

# === パス設定 ===
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
input_dir = project_root / "preprocess" / "label_editor"

# === クラス数カウント ===
class_counter = Counter()
txt_files = list(input_dir.glob("*.txt"))

print(f"処理対象ファイル数: {len(txt_files)}\n")

for txt_path in txt_files:
    lines = txt_path.read_text(encoding="utf-8").splitlines()
    for line in lines:
        if line.strip() == "":
            continue
        class_id = line.strip().split()[0]
        class_counter[class_id] += 1

# === 結果表示 ===
if class_counter:
    print("=== クラス別件数 ===")
    for class_id, count in sorted(class_counter.items(), key=lambda x: int(x[0])):
        print(f"クラス {class_id}: {count} 件")
else:
    print("クラス情報が見つかりませんでした。")

print("\n完了！")
