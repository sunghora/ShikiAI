# LE_remove_duplicates_and_move.py
# 重複ラベルの削除と、ペア画像の label_editor_output への移動処理

from pathlib import Path
import shutil

# === IOU計算関数 ===
def compute_iou(box1, box2):
    x1_min = box1[0] - box1[2] / 2
    x1_max = box1[0] + box1[2] / 2
    y1_min = box1[1] - box1[3] / 2
    y1_max = box1[1] + box1[3] / 2

    x2_min = box2[0] - box2[2] / 2
    x2_max = box2[0] + box2[2] / 2
    y2_min = box2[1] - box2[3] / 2
    y2_max = box2[1] + box2[3] / 2

    xi1 = max(x1_min, x2_min)
    yi1 = max(y1_min, y2_min)
    xi2 = min(x1_max, x2_max)
    yi2 = min(y1_max, y2_max)
    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)

    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)
    union_area = box1_area + box2_area - inter_area

    return inter_area / union_area if union_area != 0 else 0

# === パス定義 ===
shiki_root = Path(__file__).resolve().parent.parent
label_dir = shiki_root / "preprocess" / "label_editor"
output_dir = shiki_root / "preprocess" / "label_editor_output"
output_dir.mkdir(parents=True, exist_ok=True)

image_exts = [".jpg", ".jpeg", ".png"]

# === 統計用 ===
total_duplicates = 0
files_modified = 0

# === メイン処理 ===
txt_files = sorted(label_dir.glob("*.txt"))

for txt_path in txt_files:
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            continue
        class_id = int(parts[0])
        coords = list(map(float, parts[1:]))
        entries.append((class_id, coords))

    keep = []
    skip_idx = set()
    local_duplicates = 0

    for i in range(len(entries)):
        if i in skip_idx:
            continue
        c1, box1 = entries[i]
        for j in range(i + 1, len(entries)):
            if j in skip_idx:
                continue
            c2, box2 = entries[j]
            if c1 != c2:
                continue
            iou = compute_iou(box1, box2)
            print(f"    → IoU({i},{j}) = {iou:.3f}  [{txt_path.name}]")
            if iou >= 0.3:
                area1 = box1[2] * box1[3]
                area2 = box2[2] * box2[3]
                if area1 >= area2:
                    skip_idx.add(j)
                else:
                    skip_idx.add(i)
                local_duplicates += 1

        if i not in skip_idx:
            keep.append((c1, box1))

    # 修正があったら書き戻し
    if local_duplicates > 0:
        with open(txt_path, "w", encoding="utf-8") as f:
            for cls, box in keep:
                f.write(f"{cls} {' '.join(f'{v:.6f}' for v in box)}\n")

        total_duplicates += local_duplicates
        files_modified += 1
        print(f"[修正] {txt_path.name} - 重複: {local_duplicates}")

    # === 出力先に移動（.txt と画像）===
    dest_txt = output_dir / txt_path.name
    if dest_txt.exists():
        print(f"[スキップ] {dest_txt.name} は既に存在します（.txt）")
    else:
        shutil.move(str(txt_path), dest_txt)
        print(f"[移動] {txt_path.name} → {dest_txt.name}")

    base = txt_path.stem
    for ext in image_exts:
        img_file = label_dir / f"{base}{ext}"
        dest_img = output_dir / img_file.name
        if img_file.exists():
            if dest_img.exists():
                print(f"[スキップ] {dest_img.name} は既に存在します（画像）")
            else:
                shutil.move(str(img_file), dest_img)
                print(f"[移動] {img_file.name} → {dest_img.name}")

# === 結果表示 ===
print("\n✅ 全ファイルの重複除去と移動が完了しました。")
print(f"🔁 削除された重複ラベル数：{total_duplicates}")
print(f"📝 修正されたファイル数　　：{files_modified}")
print(f"📦 移動先ディレクトリ　　　：{output_dir}")
