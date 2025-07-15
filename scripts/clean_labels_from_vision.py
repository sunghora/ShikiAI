# clean_labels_from_vision.py
from pathlib import Path
import csv

# === 設定 ===
crops_dir = Path("crops")
annotations_dir = Path("annotations/datasetA")
result_csv = crops_dir / "vision_results.csv"

# === 判定結果の読み込み ===
with open(result_csv, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    result_rows = list(reader)

# === 削除対象をまとめる ===
removal_dict = {}  # {label_path: [削除するbbox行番号]}

for row in result_rows:
    result = row["result"].strip().lower()
    if result in ["no", "いいえ。"]:
        label_path = annotations_dir / row["label_file"]
        bbox_index = int(row["bbox_index"])
        removal_dict.setdefault(label_path, []).append(bbox_index)

# === ラベルファイルの修正 ===
for label_path, remove_indices in removal_dict.items():
    if not label_path.exists():
        print(f"[スキップ] {label_path.name} → ファイルなし")
        continue

    with open(label_path, encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = [line for i, line in enumerate(lines) if i not in remove_indices]

    with open(label_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"[修正] {label_path.name} → {len(remove_indices)} bbox 削除")

print("\n[完了] 誤検出アノテーションの削除完了！")
