import torch
import cv2
import os

# クラスidの名前と色のマップ
def initialize_class_and_color_maps():
    
    class_map = {
        1: 'Person',
        2: 'Bicycle',
        3: 'Car',
        4: 'Motorbike',
        6: 'Bus',
        14: 'Benches',
        17: 'Dog',
        26: 'umbrella',
    }
    color_map = {
        1: (0, 255, 0),       # Person - 緑
        2: (255, 0, 0),       # Bicycle - 青
        3: (0, 0, 255),       # Car - 赤
        4: (255, 255, 0),     # Motorbike - シアン
        6: (255, 0, 255),     # Bus - マゼンタ
        14: (0, 0, 255),      # Benches - 赤
        17: (255, 255, 255),  # Dog - 白
        26: (128, 128, 128),  # umbrella - グレー
    }
    return class_map, color_map


def draw_detections(img, detections, class_map, color_map, trajectory_map, confidence_threshold=0.50):
    
    for *box, conf, cls in detections:
        if conf >= confidence_threshold:
            x1, y1, x2, y2 = map(int, box)
            class_id = int(cls.item()) + 1

            if class_id in class_map:
                label = class_map[class_id]
                color = color_map.get(class_id, (0, 255, 0))

                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                trajectory_map[class_id].append((center_x, center_y))
                # BBの描画
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                # Class名の描画
                cv2.putText(img, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2) 
                # .putText(画像, テキスト, 座標, フォント, サイズ, 色, 太さ) cv2.FONT_HERSHEY_SIMPLEXというのは、フォントの種類のこと、
                
    for class_id, points in trajectory_map.items():
        # .iten() は 辞書のキーと値を返却するメソッド
        if class_id in color_map:
            for j in range(1, len(points)):
                cv2.circle(img, points[j], 2, color_map[class_id], -1)
                # .circle(画像, 座標, 半径, 色, 塗りつぶし) 