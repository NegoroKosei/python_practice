import pyxel


class App:
    def __init__(self): # 初期化
        pyxel.init(160, 120, title="my Game") # 画面サイズ、タイトル
        pyxel.load("my_resource.pyxres") # リソースファイルの読み込み
        self.score = 0
        self.player_x = 72
        self.player_y = 60 - 8
        self.player_dy = 0  # プレイヤーのy座標の変化量
        self.is_alive = True   # プレイヤーが生きているかどうか
        self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        # 床とフルーツは等間隔で配置(60*4 = 240 で画面幅を超える)
        self.enemy = [(i * 60 + pyxel.rndi(0, 40), pyxel.rndi(8, 104), True) for i in range(4)] # (x,y,is_alive)のリスト
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q): #Qキーで終了
            pyxel.quit()

        self.update_player() # プレイヤーの更新

        for i, v in enumerate(self.enemy): # 床の更新,enumerate関数でインデックスと値を取得(ポインタを管理しやすい)
            self.enemy[i] = self.update_enemy(*v)

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT): # 左キーかゲームパッドの左ボタンが押されたら
            self.player_x = max(self.player_x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT): # 右キーかゲームパッドの右ボタンが押されたら
            self.player_x = min(self.player_x + 2, pyxel.width - 16)
        
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP): # 上キーかゲームパッドの上ボタンが押されたら
            self.player_y = max(self.player_y - 4, 0)
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN): # 下キーかゲームパッドの下ボタンが押されたら
            self.player_y = min(self.player_y + 4, pyxel.height - 16)

        # プレーヤーの画面外判定
        # if self.player_y > pyxel.height:
        #     if self.is_alive:
        #         self.is_alive = False
        #         pyxel.play(3, 5)
        #     if self.player_y > 600:
        #         self.score = 0
        #         self.player_x = 72
        #         self.player_y = -16
        #         self.player_dy = 0
        #         self.is_alive = True

    def update_enemy(self, x, y, is_alive): # selfでクラスを受け取る
        if is_alive:
            if (
                self.player_x + 16 >= x
                and self.player_x <= x + 16
                and self.player_y + 16 >= y
                and self.player_y <= y + 16
            ):
                is_alive = False # プレイヤーが床に乗ったら床を消す
                self.score += 10
                # self.player_dy = -12 # プレイヤーをジャンプ
                # pyxel.play(3, 3)
        # 消えた場合は床を下に移動
        # else:
        #     y += 6
        # 床を左に移動,速さ4
        x -= 4
        #画面外に出たらyランダムで再配置
        if x < -40:
            x += 240
            y = pyxel.rndi(8, 104)
            is_alive = True
        return x, y, is_alive

    # blt関数で画像を描画(表示するx座標,表示するy座標,画像番号(1～3),左上のx座標,左上のy座標,幅,高さ,(透過色))
    def draw(self):
        pyxel.cls(12)

        # Draw clouds(far...32*8, near...56*8),(1/16の速さ,1/8の速さ)
        offset = (pyxel.frame_count // 2) % 160
        for i in range(2):
            for x, y in self.far_cloud:
                pyxel.rect(x + i * 160 - offset, y, 32, 8, 6)

        # Draw floors(40*8)
        for x, y, is_alive in self.enemy:
            if is_alive:
                pyxel.blt(x, y, 0, 16, 0, 16, 16, 7)

        # Draw player(上に進むときはイラストを変える)
        pyxel.blt(
            self.player_x,
            self.player_y,
            0,
            0,
            0,
            -16,
            16,
            0,
        )

        # Draw score
        s = f"SCORE {self.score:>4}"
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)


App()
