import time
from multiprocessing import Pool, Process

def nijou(inputs):
    x = inputs
    print('input: %d' % x)
    time.sleep(2)  # Simulating a time-consuming task
    retValue = x * x
    print('double: %d' % retValue)
    return retValue

if __name__ == "__main__":

    # Pool()を定義
    p = Pool()

    # プロセスを2つ非同期で実行
    result = p.apply_async(nijou, args=[3])
    result2 = p.apply_async(nijou, args=[5])

    # 結果が準備できるまで待機
    print(result.get())   # ブロックして結果を待つ
    print(result2.get())  # ブロックして結果を待つ

    # プールを閉じて終了
    p.close()
    p.join()


