import cv2
import numpy as np
import pandas as pd

# バウンディングボックスの計算, labelの変換 ==================================================================
# ======================================================================================================

def calculate_bounding_boxes(frame_data):
    
    # frame_dataの読み込み ===============================================================================
    bboxes = []
    labels = []
    ids = frame_data['id'].astype(int)
    lefts = frame_data['BB_left'].astype(float)
    tops = frame_data['BB_top'].astype(float)
    widths = frame_data['BB_width'].astype(float)
    heights = frame_data['BB_height'].astype(float)
    classes = frame_data['Class'].astype(int)
    
    # バウンディングボックスデータの整形　======================================================================
    # cv2 の .rectangle() メソッドに合わせて、(left, top, right, bottom) の形式に変換

    for left, top, width, height, class_id in zip(lefts, tops, widths, heights, classes):
        # in zip() は、複数のリストを同時にループするための関数
        right = left + width
        bottom = top + height
        bboxes.append((int(left), int(top), int(right), int(bottom)))
        
        # Class番号からClass名に変換 ======================================================================
        label_map = {
            '1': 'Pedestrian',
            '2': 'Person on a vehicle',
            '3': 'Car',
            '4': 'Bycicle',
            '5': 'Motorbike',
            '6': 'Non motorized vehicle',
            '7': 'Static person',
            '8': 'Distractor',
            '9': 'Occluder',
            '10': 'Occluder on the ground',
            '11': 'Occluder full',
            '12': 'Reflection'
        }
        label = label_map.get(str(class_id), 'Unknown')
        labels.append(label)
    
    return bboxes, labels, ids


# バウンディングボックス, 軌跡の描画関数 =====================================================================
# ======================================================================================================

def draw_trajectory_and_bounding_boxes(image, trajectory, bboxes, labels, ids, x_range, y_range):
    
    for bbox, label, id_val in zip(bboxes, labels, ids):
        left, top, right, bottom = bbox
        
        # 画像の範囲外にあるバウンディングボックスは無視
        if right < x_range[0] or left > x_range[1] or bottom < y_range[1] or top > y_range[0]:
            continue
        
        id_val = int(id_val)
        np.random.seed(id_val)
        #idvalをシードにすることで、同じidvalの場合に同じ色を取得するように
        border_color = np.random.randint(0, 255, 3).tolist() # ndarrayをリストに変換
        
        # バウンディングボックスを描画
        cv2.rectangle(image, (left, top), (right, bottom), border_color, 2)
        # .rectangle(画像, 左上座標, 右下座標, 色, 線の太さ)
        
        # ラベルを描画
        label_position = (left, top - 10 if top - 10 > 10 else top + 10)
        # ラベル位置はBBの左上、10px上になければ、その10px下に表示。
        cv2.putText(image, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, border_color, 2)
        
        # 中心座標を計算
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2
        
        # 軌跡を記録
        if id_val in trajectory:
            trajectory[id_val].append((center_x, center_y))
        else:
            trajectory[id_val] = [(center_x, center_y)]
    
    
    # 軌跡を描画
    for id_val, points in trajectory.items():
        np.random.seed(id_val) 
        border_color = np.random.randint(0, 255, 3).tolist()
        
        for j in range(1, len(points)):
            cv2.line(image, points[j - 1], points[j], border_color, 2)
            # .line(画像, 始点, 終点, 色, 線の太さ)　つまり、前回の座標から今回の座標まで線を引く
            
            
# gate1 →　左端にありそうな道をゲートとして通過したかどうかを判定する関数 ================================================
#==============================================================================================================

def gate1_detections(output_file, i, trajectory, bboxes, labels, ids):
    
    # gate1は画像の左上から左下にかけてのゲート
    gate1 = [(20, 0), (20, 1080)]
    
    for id_val, points in trajectory.items():
        if len(points) > 1:
            prev_x, prev_y = points[-2]
            curr_x, curr_y = points[-1]
            
            # 右向きに通過 (画像座標は左上が原点のため)
            if prev_x < gate1[0][0] and curr_x >= gate1[0][0]:
                direction = 'right'
                output_file.write(f"{i},{id_val},{labels[ids.tolist().index(id_val)]},{direction}\n")
                
            # 左向きに通過
            if prev_x > gate1[0][0] and curr_x <= gate1[0][0]:
                direction = 'left'
                output_file.write(f"{i},{id_val},{labels[ids.tolist().index(id_val)]},{direction}\n")
                