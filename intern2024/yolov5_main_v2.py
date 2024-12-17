import torch
import cv2
import os
from yolov5_mods_v2 import  initialize_class_and_color_maps, draw_detections

# モデルの読み込み
model =model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)

# tourch.hub.load() は、指定されたリポジトリからモデルをダウンロードして読み込む
# 第1引数: リポジトリの名前（'ultralytics/yolov5'）, 第2引数: モデルの名前（'yolov5s'）, 第3引数: 事前学習済みのモデルを使用するかどうか（pretrained=True）

# 初回はダウンロードされるが、2回目以降は、 .ptファイルから読み込まれる。
# .pt ファイルは PyTorch のモデルファイルの拡張子で、モデルの重みや構造を保存するためのファイル形式

# モデルについて =======================================================================
# yolov5n →　yolov5s →　yolov5m →　yolov5l →　yolov5x .pt 
#　n → x でモデルの精度が上がるが、計算量も増える(処理速度が下がる)
# ====================================================================================

class_map, color_map = initialize_class_and_color_maps() #クラスとカラーの辞書を受け渡す。

# 出力フォルダの確認
output_folder = '12月8日/img1_BB'
if not os.path.exists(output_folder):
    print(f"Output folder {output_folder} not found.")

# 軌跡を記録する辞書
trajectory_map = {i: [] for i in class_map.keys()} #クラスmapのキーで空のリストを作成

# 画像処理ループ
for i in range(1, 601):
    img_path = f'12月8日/img1/{i:06d}.jpg'
    img = cv2.imread(img_path)

    if img is None: 
        print(f"Image {img_path} not found.")
        continue
    
    
    results = model(img) #モデルに画像を入力して結果を取得
    detections = results.xyxy[0] #BBの左上、右下の座標検知, 信頼度, クラスid
    
    draw_detections(img, detections, class_map, color_map, trajectory_map)
    
    # 画像の保存
    output_path = os.path.join(output_folder, f"{i:06d}.jpg")
    cv2.imwrite(output_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    print(f"Saved {output_path}")
