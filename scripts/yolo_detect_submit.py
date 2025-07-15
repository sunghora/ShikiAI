# yolo_detect_submit.py
# 提出画像136枚に特化した最終調整用ファインチューニングスクリプト
# ベースモデルはexp22のbest.pt、全ての画像をtrainとして使用（valなし）

from ultralytics import YOLO

def main():
    # 提出特化：exp22のベストモデルをファインチューニング
    model = YOLO('runs/detect_exp22/weights/best.pt')  # パスは必要に応じて調整

    model.train(
        epochs=25,             # 軽めのエポックで過学習回避＆高速完了
        batch=8,               # 少量データに合わせた小バッチ
        imgsz=1024,
        lr0=0.0005,            # 微調整用の低LR
        patience=8,            # 早期打ち切りも可能に
        hsv_h=0.0,
        hsv_s=0.0,
        hsv_v=0.0,
        degrees=0.0,
        translate=0.05,
        scale=0.8,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.0,
        mosaic=0.0,
        mixup=0.0,
        data='ShikiAI_submit_data.yaml',  # 提出画像専用データ定義
        name='detect_submit',
        device=0,
        workers=4,
        project='runs',
        exist_ok=True,
        resume=False,
        cache=True
    )

if __name__ == '__main__':
    main()
