####### 並列計算を使えるように ############
from multiprocessing import Pool

####### aとbを掛け算するだけの関数 #########
def kakezan(a, b):
    return a*b

####### ラッパー ######
# 並列処理をするために引数を1つにまとめる
def wrapper_kakezan(args):
    return kakezan(*args)

####### 並列処理実行 ########
if __name__ == "__main__":
    tutumimono = [[i, 3] for i in range(1000)]
    # Pool()を定義、プロセスを2つ非同期で実行
    p = Pool(processes=2)
    # 結果が準備できるまで待機
    print( p.map(wrapper_kakezan, tutumimono) )