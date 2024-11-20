# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
from common.functions import *
from common.gradient import numerical_gradient
import numpy as np

class TwoLayerNet:

    def __init__(self, input_size, hidden_size, output_size, weight_init_std=0.01):
        # 重みの初期化
        # paramsは、ニューラルネットワークのパラメータを保持するディクショナリ変数
        self.params = {}
        self.params['W1'] = weight_init_std * np.random.randn(input_size, hidden_size)
        self.params['b1'] = np.zeros(hidden_size)
        self.params['W2'] = weight_init_std * np.random.randn(hidden_size, output_size)
        self.params['b2'] = np.zeros(output_size)
        
    def predict(self, x):
        # 2層のニューラルネットワークの推論処理
        
        W1, W2 = self.params['W1'], self.params['W2']
        b1, b2 = self.params['b1'], self.params['b2']
    
        # 入力層(1層目)から隠れ層(2層目)への計算では、重みW1とバイアスb1を使い、二層目の入力値:a1を計算
        # そして、活性化関数sigmoid()を使って、a1から2層目の出力値:z1を計算
        a1 = np.dot(x, W1) + b1
        z1 = sigmoid(a1)
        
        # 隠れ層(2層目)から出力層(3層目)への計算では、重みW2とバイアスb2を使い、3層目の入力値:a2を計算
        # そして、活性化関数softmax()を使って、a2から出力値:yを計算
        a2 = np.dot(z1, W2) + b2
        y = softmax(a2)
        # ↑ 出力層で利用する活性化関数は、回帰問題の場合は恒等関数、分類問題の場合はソフトマックス関数を使うのが一般的
        
        return y
        
    # x:入力データ, t:教師データ
    def loss(self, x, t):
        y = self.predict(x)
        # .predict(x)で入力データxをニューラルネットワークに入力し、出力yを得る
        
        return cross_entropy_error(y, t)
    
    def accuracy(self, x, t):
        y = self.predict(x)
        y = np.argmax(y, axis=1)
        t = np.argmax(t, axis=1)
        
        accuracy = np.sum(y == t) / float(x.shape[0])
        return accuracy
        
    # x:入力データ, t:教師データ
    def numerical_gradient(self, x, t):
        loss_W = lambda W: self.loss(x, t)
        
        # gradsは、各層における重みを保持するディクショナリ変数
        # numerical_gradient(f, x)は、関数f(x)におけるxの勾配を求める関数 commonディレクトリ下にある。
        grads = {}
        grads['W1'] = numerical_gradient(loss_W, self.params['W1'])
        grads['b1'] = numerical_gradient(loss_W, self.params['b1'])
        grads['W2'] = numerical_gradient(loss_W, self.params['W2'])
        grads['b2'] = numerical_gradient(loss_W, self.params['b2'])
        
        return grads
    
    def gradient(self, x, t):
        # 誤差逆伝播法によって勾配を求める　5章で詳しく説明
        W1, W2 = self.params['W1'], self.params['W2']
        b1, b2 = self.params['b1'], self.params['b2']
        grads = {}
        
        batch_num = x.shape[0]
        
        # forward
        a1 = np.dot(x, W1) + b1
        z1 = sigmoid(a1)
        a2 = np.dot(z1, W2) + b2
        y = softmax(a2)
        
        # backward
        dy = (y - t) / batch_num
        grads['W2'] = np.dot(z1.T, dy)
        grads['b2'] = np.sum(dy, axis=0)
        
        dz1 = np.dot(dy, W2.T)
        da1 = sigmoid_grad(a1) * dz1
        grads['W1'] = np.dot(x.T, da1)
        grads['b1'] = np.sum(da1, axis=0)

        return grads
