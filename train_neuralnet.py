# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
import matplotlib.pyplot as plt
from dataset.mnist import load_mnist  # dataset/mnist.pyからload_mnist関数をインポート
from two_layer_net import TwoLayerNet # two_layer_net.pyからTwoLayerNetクラスをインポート

# MINISTデータセットの読み込み
# 今回は、訓練データをx_train、訓練データのラベルをt_train、テストデータをx_test、テストデータのラベルをt_testとして読み込む
(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True) 
# print(x_train.shape) # (60000, 784) → 28x28=784
# print(t_train.shape) # (60000, 10)  → 0~9の数字をone-hot表現で表すため、10次元の配列

network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

iters_num = 10000  # 繰り返しの回数を適宜設定する
train_size = x_train.shape[0] # = 訓練データの個数 = 60000
batch_size = 100
learning_rate = 0.1

train_loss_list = []
train_acc_list = []
test_acc_list = []

iter_per_epoch = max(train_size / batch_size, 1)

for i in range(iters_num):
    # 60000個の訓練データからランダムに100(batch_size)個のデータを抽出
    batch_mask = np.random.choice(train_size, batch_size) # 0~59999の範囲からランダムに100個の数字を抽出
    
    # ミニバッチの作成
    x_batch = x_train[batch_mask]
    t_batch = t_train[batch_mask]
    
    # 勾配の計算
    # grad = network.numerical_gradient(x_batch, t_batch)
    grad = network.gradient(x_batch, t_batch)
    
    # パラメータの更新
    for key in ('W1', 'b1', 'W2', 'b2'):
        network.params[key] -= learning_rate * grad[key] # p107の式(4.7):勾配降下法の更新式
    
    # 誤差関数の値の計算
    # →　現在の"重み"を用いた出力クラスの予測を、loss関数の中のpredict関数で行い、誤差との評価をする
    loss = network.loss(x_batch, t_batch)
    train_loss_list.append(loss)
    
    # 1エポックごとに認識精度を計算
    if i % iter_per_epoch == 0:
        train_acc = network.accuracy(x_train, t_train)
        test_acc = network.accuracy(x_test, t_test)
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)
        print("train acc, test acc | " + str(train_acc) + ", " + str(test_acc))
        

# # 損失関数の値の推移 ===========================================
# x = np.arange(len(train_loss_list))
# plt.plot(x, train_loss_list)
# plt.xlabel("iterations")
# plt.ylabel("loss")
# plt.show()

# グラフの描画 ===================================================
# markers = {'train': 'o', 'test': 's'}
# x = np.arange(len(train_acc_list))
# plt.plot(x, train_acc_list, label='train acc')
# plt.plot(x, test_acc_list, label='test acc', linestyle='--')
# plt.xlabel("epochs")
# plt.ylabel("accuracy")
# plt.ylim(0, 1.0)
# plt.legend(loc='lower right')
# plt.show()

# 学習パラメータを用いて、i番目の画像を予測する ======================
i = 10
img = x_test[i]
label = t_test[i]
pred = network.predict(img)
print("label: " + str(label))
print("pred: " + str(pred))
print("pred: " + str(np.argmax(pred)))

# 画像を表示
img = img.reshape(28, 28)
plt.imshow(img, cmap='gray')
plt.show()
