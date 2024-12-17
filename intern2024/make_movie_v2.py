import glob
import re
import cv2

# 入力画像フォルダと出力動画のパス
input_path = '10月26日/MOT17-02-DPM/img1_bbox/'
output_path = '10月26日/MOT17-02-DPM/img1_bbox.mp4'

# 画像データの取得
pic_list = glob.glob(input_path + "*.jpg")  # jpgファイルをすべて取得
pic_list.sort(key=lambda x: int(re.search(r"(\d+).jpg", x).group(1)))

# 動画作成の準備
if not pic_list:
    raise ValueError("No images found in the specified directory.")

# サンプル画像を1枚読み込み、動画の解像度を取得
sample_img = cv2.imread(pic_list[0])
height, width, layers = sample_img.shape

# 動画出力の設定
fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H.264用の"コーデック"を使用
fps = 25  # フレームレート
video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# 動画生成
print("Starting video generation...")
for i, file in enumerate(pic_list):
    frame = cv2.imread(file)  # 画像を読み込み
    video_writer.write(frame)  # フレームを追加

    # 進捗表示
    print(f"Processing frame {i+1}/{len(pic_list)}")

# 動画ファイルを閉じる
video_writer.release()
print(f"Video saved to {output_path}")
