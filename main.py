import gc
from yanesdk import *
from meigen import author,told


# 基底クラスはどちらも__init__を持たず、onDrawのみを持っている。
# いずれも派生クラスでオーバーライドして必要な処理を実装する。
# ゲームオブジェクトの基底クラス
class MyGameObject(GameObject):
    def onDraw(self, app:'TheApp'):
        pass

# シーンの基底クラス
class Scene:
    def onDraw(self, app:'TheApp'):
        pass


# 以下はゲームオブジェクト----------------------------

# 本
class Book(MyGameObject):
    def __init__(self, app:'TheApp', p:Vector2D, v:Vector2D, title:str, size:int):
        super().__init__()
        # 座標
        self.p = p
        # ベクトル
        self.v = v
        # タイトル
        self.title = title
        # フォントサイズ
        self.size = size

    def onDraw(self, app:"TheApp"):
        if self.deleted == True:
            del app.titles[0]
            gc.collect()
        # 描画
        canvas = app.canvas
        # タイトルが生まれるところを見せたくないのでVector2D(0,int(app.canvas.height*0.1))分だけ上で生成
        yohaku = int(canvas.height*0.1)
        canvas.draw_text_center(self.title, self.p+Vector2D(0,-yohaku), font=f"{self.size}px serif", color=app.color[app.wordcolor])
        # 移動
        self.p += self.v
        # 画面範囲外に出たものは削除。
        # canvasそのものの範囲を指定すると突然消えてしまうように見えるので、yohakuを足している
        self.deleted = not self.p.is_in_rect(Rect(Vector2D(0,-yohaku), Vector2D(canvas.width, canvas.height+yohaku*2)))


# 本のマネージャー
class BookManager(MyGameObject):

    def __init__(self):
        # 進行フレーム数を記録する変数
        # 60fpsなので、1秒間に60フレーム増える（1秒で60cntとなる）。
        self.cnt = 0
    
    def onDraw(self, app:'TheApp'):
        # このメソッドは、GameMainSceneからしか呼び出さない。
        scene = cast(GameMainScene, app.scene)
        # cntをイテレーション
        self.cnt += 1
        # 表示するタイトルのリスト
        books = scene.books

        if app.flg == False: 
            # ウェルカムメッセージの表示
            welcom_size = int(30*app.canvas.width/1920)
            center_width = app.canvas.width//2
            center_height = app.canvas.height//2
            size = app.math.randint(welcom_size, welcom_size)
            p = Vector2D(center_width, center_height*0.95)
            pp = Vector2D(center_width, center_height*1.05)
            app.canvas.draw_text_center(told, p, font=f"{size}px serif", color=app.color[app.wordcolor])
            app.canvas.draw_text_center(author, pp, font=f"{size//2}px serif", color=app.color[app.wordcolor])
            app.flg = True

        else:
            # タイトルの読み込み
            if app.fflg == False:
                import req
                app.titles = req.titles
                app.fflg == True
            app.lentitles = len(app.titles)
            # タイトルを書き込む範囲
            rect = app.canvas.rect

            # タイトルを生成する処理
            if self.cnt%15 == 0:
                scene = cast(GameMainScene, app.scene)
                # 文字の横位置、フォントサイズ、タイトルをランダム指定
                maxnum = int(60*app.canvas.width/1920)
                minnum = int(10*app.canvas.width/1920)
                size = app.math.randint(minnum, maxnum)
                p = Vector2D(app.math.randint(0, int(rect.s.x)), 0)
                title = app.titles[app.math.randint(0, app.lentitles)]
                # 速度は一定
                v = Vector2D(0,0.016*size+0.84)
                # インスタンス追加
                books.append(Book(app,p,v,title,size))


# メイン画面
class GameMainScene(Scene):
    def __init__(self):
        # 描画中に個数が増減するインスタンスを管理するスタックはGameobjectManager()として定義。
        # そのスタックの中にインスタンスを入れる。消すときはスタックからの削除とインスタンスのdeletedをTrueにする。
        # ゲーム中で個数が一定のインスタンスはGameobjectを継承したインスタンスを作成。

        # 描画する本のリスト
        self.books = GameObjectManager()

        # 描画優先順位の逆順で登録しておく。(その順番で呼び出したいので)
        self.draw_objects = (
            self.books,
            # ここでゲームにただひとつだけ必要なインスタンスを生成する。
            # initはここでしか呼ばれない。
            BookManager(), 
        )

    #ここで各gameobjectのondrawの処理が呼ばれる
    def onDraw(self, app:"TheApp"):
        # スクリーンのクリアと画面幅の調整
        # canvasの引数にcolorを入れるとcanvasの背景色を指定できる。          
        app.canvas.clear(color=app.color[app.backcolor])

        # スペースキー相当のキーが押されたら色反転
        app.keyinput.update()
        if app.keyinput.is_key_pushed(VKEY.SPACE):
            app.backcolor = (-app.backcolor+1)
            app.wordcolor = (-app.wordcolor+1)

        # 描画優先順位の逆順で描画していく。
        for object in self.draw_objects:
            object.onDraw(app)

    
# ゲームアプリのメインコントローラ
class TheApp(GameContext):
    def __init__(self):

        # 描画用スクリーン
        self.canvas = Canvas()

        # 数学関連のツール
        self.math = MathTools()
        
        # 最初に遷移すべきScene
        self.scene:Scene = GameMainScene()
        # ゲームの最終スコア記録用
        self.score = 0

        # タイトル
        self.titles = []
        self.lentitles = 0

        # ウェルカムメッセージのフラグ
        self.flg = False
        self.fflg = False

        # 文字色と背景色
        self.color = {0:'black',1:'white'}
        self.wordcolor = 0
        self.backcolor = 1
        # 色反転用コントローラ
        self.keyinput = VirtualKeyInput()
        self.keyinput.configure_1key_game()

        # 音声ファイル
        # audio_loader = AudioLoader(Audio.audio_file_list)
        # self.audios = audio_loader.audios
        # 描画のloop
        self.gametimer = GameTimer(lambda : self.scene.onDraw(self), fps=75)


if __name__ == '__main__':
    try:
        TheApp()
    except:
        InfoDialog('エラーが発生しました。', traceback.format_exc())
    