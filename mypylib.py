import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
import matplotlib.font_manager as fm
import os


def scatter_graph(data_list, xlabel="X-axis", ylabel="Y-axis", title=None, xrange=None, yrange=None, output_path=None):
    """
    リスト形式のデータを受け取り、それぞれのデータを散布図にプロットする関数。
    
    Parameters:
        data_list: list
            各データは [x, y, color, label] の形式のリスト。
            - x: x軸データ (リストまたは1次元配列)
            - y: y軸データ (リストまたは1次元配列)
            - color: 各データの色 (文字列)
            - label: 各データのラベル (文字列)
        xlabel: str
        ylabel: str
        title: str
        xrange: tuple(xmin, xmax)
        yrange: tuple(ymin, ymax)
        output_path: str
    """
    label_flag = True
    # 日本語フォントを指定 (IPAexGothicを使用)
    plt.rcParams['font.family'] = 'Meiryo'
    plt.rcParams['mathtext.fontset'] = 'cm'

    plt.figure(figsize=(5, 5))

    # デフォルトのカラーリスト（Matplotlibのデフォルトカラー）
    default_colors = [f"C{i}" for i in range(len(data_list))]
    # データごとにプロット
    for i, data in enumerate(data_list):
        if len(data) < 2 or len(data) > 4:
            raise ValueError("各データは [x, y, color, label] の形式である必要があります（color と label は任意）。")
        
        # データの分解とデフォルト値の適用
        x, y = data[0], data[1]
        color = data[2] if len(data) > 2 and data[2] is not None else default_colors[i]
        if len(data) > 3 and data[3] is not None:
            label = data[3]
        else:
            label = f"Data {i+1}"
            label_flag = False
        # 散布図をプロット
        plt.scatter(x, y, color=color, label=label, s=5)


    # 軸ラベルと凡例の設定
    plt.xlabel(xlabel, fontsize=15)
    plt.ylabel(ylabel, fontsize=15)
    plt.tick_params(direction='in', which='both')  # 'both' でx軸とy軸両方の目盛りを内向きに
    if xrange is not None:
        plt.xlim(xrange[0], xrange[1]) # X軸の範囲を調整
    if yrange is not None:
        plt.ylim(yrange[0], yrange[1])  # Y軸の範囲を調整
    if label_flag:
        plt.legend()
    if title is not None:
        plt.title(title)
    if output_path is not None:
        # 必要なフォルダパスの生成
        output_dir = os.path.dirname(output_path)  # ディレクトリ部分を抽出
        # フォルダが存在しない場合に作成
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        plt.savefig(output_path,bbox_inches='tight')
    # グラフを表示
    plt.show()


def line_graph(data_list, xlabel="X-axis", ylabel="Y-axis", title=None, xrange=None, yrange=None, output_path=None):
    """
    リスト形式のデータを受け取り、それぞれのデータを散布図にプロットする関数。

    Parameters:
        data_list: list
            各データは [x, y, color, label] の形式のリスト。
            - x: x軸データ (リストまたは1次元配列)
            - y: y軸データ (リストまたは1次元配列)
            - color: 各データの色 (文字列)
            - label: 各データのラベル (文字列)
        xlabel: str
        ylabel: str
        title: str
        xrange: tuple(xmin, xmax)
        yrange: tuple(ymin, ymax)
        output_path: str
    """
    label_flag = True
    # 日本語フォントを指定 (IPAexGothicを使用)
    plt.rcParams['font.family'] = 'Meiryo'
    plt.rcParams['mathtext.fontset'] = 'cm'


    plt.figure(figsize=(5, 5))

    # デフォルトのカラーリスト（Matplotlibのデフォルトカラー）
    default_colors = [f"C{i}" for i in range(len(data_list))]
    # データごとにプロット
    for i, data in enumerate(data_list):
        if len(data) < 2 or len(data) > 4:
            raise ValueError("各データは [x, y, color, label] の形式である必要があります（color と label は任意）。")
        
        # データの分解とデフォルト値の適用
        x, y = data[0], data[1]
        color = data[2] if len(data) > 2 and data[2] is not None else default_colors[i]
        if len(data) > 3 and data[3] is not None:
            label = data[3]
        else:
            label = f"Data {i+1}"
            label_flag = False
        # 散布図をプロット
        plt.plot(x, y, marker='o', linestyle='-', color=color, label=label, markersize=3)

    # 軸ラベルと凡例の設定
    plt.xlabel(xlabel, fontsize=15)
    plt.ylabel(ylabel, fontsize=15)
    plt.tick_params(direction='in', which='both')  # 'both' でx軸とy軸両方の目盛りを内向きに
    if xrange is not None:
        plt.xlim(xrange[0], xrange[1]) # X軸の範囲を調整
    if yrange is not None:
        plt.ylim(yrange[0], yrange[1])  # Y軸の範囲を調整
    if label_flag:
        plt.legend()
    if title is not None:
        plt.title(title)
    if output_path is not None:
        # 必要なフォルダパスの生成
        output_dir = os.path.dirname(output_path)  # ディレクトリ部分を抽出
        # フォルダが存在しない場合に作成
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        plt.savefig(output_path, bbox_inches='tight')
    # グラフを表示
    plt.show()




def load_file(file_path: str) -> np.ndarray:
    try:
        # ファイルを読み込み、'D'を'E'に置換
        with open(file_path, 'r') as file:
            data_str = file.read().replace('D', 'E')
        
        # 文字列データを数値配列に変換
        data = np.loadtxt(StringIO(data_str))
        return data
    
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

# ファイルを読み込んでDをEに置換して、特定の列を取り出す関数
def load_file_xy(file_path: str, col1: int, col2: int) -> np.ndarray:
    try:
        # ファイルを読み込み、'D'を'E'に置換
        with open(file_path, 'r') as file:
            data_str = file.read().replace('D', 'E')
        
        # 文字列データを数値配列に変換
        data = np.loadtxt(StringIO(data_str))

        # 指定された列インデックスが範囲内か確認
        if col1 >= data.shape[1] or col2 >= data.shape[1]:
            raise ValueError(f"Invalid column indices: col1={col1}, col2={col2}. Data has {data.shape[1]} columns.")
        
        # x, y列を取り出して返す
        x = data[:, col1]
        y = data[:, col2]
        return x, y
    
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    
    except ValueError as ve:
        raise ve
    
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
    

def scatter_graph2(data_list, xlabel="X-axis", ylabel="Y-axis", title=None, xrange=None, yrange=None, output_path=None):
    """
    リスト形式のデータを受け取り、それぞれのデータを散布図にプロットする関数。
    
    Parameters:
        data_list: list
            各データは [x, y, color, label] の形式のリスト。
            - x: x軸データ (リストまたは1次元配列)
            - y: y軸データ (リストまたは1次元配列)
            - color: 各データの色 (文字列)
            - label: 各データのラベル (文字列)
        xlabel: str
        ylabel: str
        title: str
        xrange: tuple(xmin, xmax)
        yrange: tuple(ymin, ymax)
        output_path: str
    """
    
    label_flag = True
    # 日本語フォントを指定 (IPAexGothicを使用)
    plt.rcParams['font.family'] = 'Meiryo'
    plt.rcParams['mathtext.fontset'] = 'cm'
    # デフォルトのカラーリスト（Matplotlibのデフォルトカラー）
    default_colors = [f"C{i}" for i in range(len(data_list))]

    fig, ax = plt.subplots(figsize=(5, 5))
    # データごとにプロット
    for i, data in enumerate(data_list):
        if len(data) < 2 or len(data) > 4:
            raise ValueError("各データは [x, y, color, label] の形式である必要があります（color と label は任意）。")
        
        # データの分解とデフォルト値の適用
        x, y = data[0], data[1]
        color = data[2] if len(data) > 2 and data[2] is not None else default_colors[i]
        if len(data) > 3 and data[3] is not None:
            label = data[3]
        else:
            label = f"Data {i+1}"
            label_flag = False
        # 散布図をプロット
        ax.scatter(x, y, color=color, label=label, s=5)


    # 軸ラベルと凡例の設定
    ax.set_xlabel(xlabel, fontsize=15)
    ax.set_ylabel(ylabel, fontsize=15)
    ax.tick_params(direction='in', which='both')  # 'both' でx軸とy軸両方の目盛りを内向きに
    if xrange is not None:
        ax.set_xlim(xrange[0], xrange[1]) # X軸の範囲を調整
    else:
        xrange = ax.get_xlim()  # x軸の範囲
    if yrange is not None:
        ax.set_ylim(yrange[0], yrange[1])  # Y軸の範囲を調整
    else:
        yrange = ax.get_ylim()
    # # アスペクト比を調整
    # data_aspect_ratio = (yrange[1] - yrange[0]) / (xrange[1] - xrange[0])  # データのアスペクト比
    # # 図のサイズ情報を取得
    # fig_width, fig_height = fig.get_size_inches()
    # figure_aspect_ratio = fig_height / fig_width  # 図全体のアスペクト比
    # # 必要な調整値を計算
    # adjustment = data_aspect_ratio / figure_aspect_ratio
    # # アスペクト比を調整して1:1に設定
    # ax.set_aspect(adjustment, adjustable='box')
    if label_flag:
        ax.legend()
    if title is not None:
        ax.set_title(title)
    if output_path is not None:
        # 必要なフォルダパスの生成
        output_dir = os.path.dirname(output_path)  # ディレクトリ部分を抽出
        # フォルダが存在しない場合に作成
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        plt.savefig(output_path,bbox_inches='tight')
    # グラフを表示
    plt.show()


def line_graph2(data_list, xlabel="X-axis", ylabel="Y-axis", title=None, xrange=None, yrange=None, output_path=None):
    """
    リスト形式のデータを受け取り、それぞれのデータを散布図にプロットする関数。

    Parameters:
        data_list: list
            各データは [x, y, color, label] の形式のリスト。
            - x: x軸データ (リストまたは1次元配列)
            - y: y軸データ (リストまたは1次元配列)
            - color: 各データの色 (文字列)
            - label: 各データのラベル (文字列)
        xlabel: str
        ylabel: str
        title: str
        xrange: tuple(xmin, xmax)
        yrange: tuple(ymin, ymax)
        output_path: str
    """
    label_flag = True
    # 日本語フォントを指定 (IPAexGothicを使用)
    plt.rcParams['font.family'] = 'Meiryo'
    plt.rcParams['mathtext.fontset'] = 'cm'

    plt.figure(figsize=(5, 5))

    # デフォルトのカラーリスト（Matplotlibのデフォルトカラー）
    default_colors = [f"C{i}" for i in range(len(data_list))]
    # データごとにプロット
    for i, data in enumerate(data_list):
        if len(data) < 2 or len(data) > 4:
            raise ValueError("各データは [x, y, color, label] の形式である必要があります（color と label は任意）。")
        
        # データの分解とデフォルト値の適用
        x, y = data[0], data[1]
        color = data[2] if len(data) > 2 and data[2] is not None else default_colors[i]
        if len(data) > 3 and data[3] is not None:
            label = data[3]
        else:
            label = f"Data {i+1}"
            label_flag = False
        # 散布図をプロット
        plt.plot(x, y, marker='o', linestyle='-', color=color, label=label, markersize=3)

    # 軸ラベルと凡例の設定
    plt.xlabel(xlabel, fontsize=15)
    plt.ylabel(ylabel, fontsize=15)
    plt.tick_params(direction='in', which='both')  # 'both' でx軸とy軸両方の目盛りを内向きに
    if xrange is not None:
        plt.xlim(xrange[0], xrange[1]) # X軸の範囲を調整
    if yrange is not None:
        plt.ylim(yrange[0], yrange[1])  # Y軸の範囲を調整
    if label_flag:
        plt.legend()
    if title is not None:
        plt.title(title)
    if output_path is not None:
        # 必要なフォルダパスの生成
        output_dir = os.path.dirname(output_path)  # ディレクトリ部分を抽出
        # フォルダが存在しない場合に作成
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        plt.savefig(output_path, bbox_inches='tight')
    # グラフを表示
    plt.show()