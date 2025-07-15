# check_with_vision.py
from pathlib import Path
import openai
import csv
import time
from dotenv import load_dotenv
import os
import base64

# === .envからAPIキーを読み込み ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY が .env に設定されていません")

openai.api_key = api_key

# === 設定 ===
crops_dir = Path("crops")
mapping_path = crops_dir / "mapping.csv"
result_path = crops_dir / "vision_results.csv"

# === Vision判定関数 ===
def is_license_plate(img_path: Path) -> str:
    with open(img_path, "rb") as f:
        image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful image classification assistant."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "これは日本の車のナンバープレートですか？YESかNOで答えてください。"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ]
                }
            ],
            max_tokens=10
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[ERROR] {img_path.name}: {e}")
        return "ERROR"

# === 対象読み込み ===
with open(mapping_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# === 出力CSV初期化 ===
with open(result_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["crop", "result", "source_image", "label_file", "bbox_index", "class_id"])

    for row in rows:
        crop_name = row["cropファイル名"]
        crop_path = crops_dir / crop_name
        result = is_license_plate(crop_path)

        writer.writerow([
            crop_name,
            result,
            row["元画像"],
            row["YOLOラベル"],
            row["bbox番号"],
            row["クラスID"]
        ])

        print(f"[判定] {crop_name} → {result}")
        time.sleep(1.5)  # 過負荷対策（必要に応じて調整）

print(f"\n[完了] Vision判定結果 → {result_path}")
