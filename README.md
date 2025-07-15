# ShikiAI

## このリポジトリについて

ShikiAIは、ナンバープレートの検出と分類を行うプロジェクトです。

### 本リポジトリに含まれるもの
- スクリプト一式（推論・前処理など）
- モデルファイル（`runs/detect_submit/weights/shiki_apex.pt`）
- 環境定義ファイル（`requirements.txt`）
- 設計書（`ShikiAI_設計書.ods`）

### 含まれていないもの
- 機密画像データ（受領画像、学習素材）
- アノテーションデータ（YOLO形式の .txt）
- 検出結果画像（bbox付きJPEGなど）

これらのファイルは `.gitignore` により除外されており、別途ZIP等で提出します。

---

詳細な構成・設計方針については、**`ShikiAI_設計書.ods`** をご参照ください。
