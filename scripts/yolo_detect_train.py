#yolo_detect_train.py  トレーニング用学習パラメータ。汎用を求める構成

from ultralytics import YOLO

def main():
    model = YOLO('yolov8m.pt')

    model.train(
        epochs=70,
        batch=24,
        imgsz=640,
        lr0=0.003,
        patience=15,
        # optimizer='auto',
        hsv_h=0.015,
        hsv_s=0.3,
        hsv_v=0.3,
        degrees=25.0,
        translate=0.3,
        scale=1.0,
        shear=0.1,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        mosaic=0.5,
        mixup=0.1,
        # model='yolov8n.pt',
        data='ShikiAI_data.yaml',
        name='detect_exp28',
        device=0,
        workers=8,
        project='runs',
        exist_ok=True,
        resume=False,
        cache=True
    )

if __name__ == '__main__':
    main()
