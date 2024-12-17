import cv2
import numpy as np
import pandas as pd


from BB_mods_v2 import calculate_bounding_boxes, draw_trajectory_and_bounding_boxes, gate1_detections

# 軌跡の記録用辞書
trajectory = {}
# inputdataの読み込み
gt_path = '10月26日/MOT17-02-DPM/gt/gt.txt'
columns = ['frame', 'id', 'BB_left', 'BB_top', 'BB_width', 'BB_height', 
           'Confi_score', 'Class', 'Visibility']

gt_data = pd.read_csv(gt_path, header=None, names=columns)

# gt_dataの中身 =====================================================
# 1列目: フレーム番号, 2列目: ID, 3列目: BB_left, 4列目: BB_top, 5列目: BB_width, 6列目: BB_height, 7列目: Confi_score, 8列目: Class, 9列目: Visibility
# ==================================================================

# 画像の範囲設定
x_range = (0, 1920)
y_range = (1080, 0)

gate1_output_path = 'gate1_data.csv'
with open(gate1_output_path, 'w') as gate1_output_file:

    for i in range(1, 601):
        img_path = f'10月26日/MOT17-02-DPM/img1/{i:06d}.jpg'
        image = cv2.imread(img_path)
        # 画像が存在しない場合はスキップ
        if image is None:
            print(f"Image {img_path} not found.")
            continue
        # フレームデータを取得
        frame_data = gt_data[gt_data['frame'] == i]

        # バウンディングボックスを計算
        bboxes, labels, ids = calculate_bounding_boxes(frame_data)

        # バウンディングボックスと軌跡を描画
        draw_trajectory_and_bounding_boxes(image, trajectory, bboxes, labels, ids, x_range, y_range)

        gate1_detections(gate1_output_file, i, trajectory, bboxes, labels, ids)

        # 画像を保存
        save_path = f'10月26日/MOT17-02-DPM/img1_bbox/{i:06d}.jpg'
        cv2.imwrite(save_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        # .write(保存先, 画像, [保存形式, 保存品質]) 100が最高
        print(f"Saved {save_path}")