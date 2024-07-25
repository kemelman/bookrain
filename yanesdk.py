# ==============================================================================
#                     Yaneurao Game SDK for Brython V1.10
# ==============================================================================

#  required : Python version >= 3.10

from browser import document, window , DOMEvent # type:ignore
from browser.widgets.dialog import Dialog, EntryDialog, InfoDialog # type:ignore

from enum import IntEnum
from typing import Callable, Generator, cast # type:ignore
import traceback
import math
import random
from timeit import default_timer as timer

# ------------------------------------------------------------------------------
#                              数学関係のツール
# ------------------------------------------------------------------------------

# 数学関係のツール
class MathTools:

    # 円周率(定数)
    PI:float = math.pi

    # xを区間[min,max]の範囲に収める
    @staticmethod
    def clamp(x:int | float, min:int | float, max: int | float)-> int | float:
        if x < min:
            x = min
        if x > max:
            x = max
        return x

    # 区間[min,max)の整数の乱数を返す。
    # maxが指定されなかった場合は、区間[0,min)の整数の乱数を返す。
    @staticmethod
    def randint(min:int,max:int | None=None)->int:
        if max:
            return math.floor(random.random() * (max - min)) + min
        return math.floor(random.random() * min)

    # sin関数。単位は角度(360を指定すると2π[rad])
    @staticmethod
    def sin_deg(x:int | float)->float:
        return math.sin(math.pi*2 * x / 360)

    # sin関数。単位はrad。
    @staticmethod
    def sin(x:float)->float:
        return math.sin(x)

    # cos関数。単位は角度(360を指定すると2π[rad])
    @staticmethod
    def cos_deg(x:int | float)->float:
        return math.cos(math.pi*2 * x / 360)

    # cos関数。単位はrad。
    @staticmethod
    def cos(x:int | float)->float:
        return math.cos(x)

    # ベクトルの方向を0-360で返す。(右方向が0、上方向(スクリーン座標での上なのでVector2D(0,-1)が上方向であることに注意) が90、..)
    @staticmethod
    def atan_deg(v:"Vector2D")->float:
        # JavaScriptのatan2は 区間[-π,+π](-180°～180°)の範囲で返ってくるので360足して 360で割ったあまりを考えることで補整。
        return (360 - math.atan2(v.y, v.x) * 180 / math.pi) % 360

# ------------------------------------------------------------------------------
#                              図形関連
# ------------------------------------------------------------------------------

# 2次元ベクトル
# このclassはimmutable
class Vector2D:
    def __init__(self, x:int | float = 0, y:int | float = 0):
        self._x = x
        self._y = y

    # readonly
    @property
    def x(self)->int | float:
        return self._x

    # readonly
    @property
    def y(self)->int | float:
        return self._y

    # operator ==
    def __eq__(self, other:object)->bool:
        other_ = cast(Vector2D,other)
        return self._x == other_._x and self._y == other_._y

    # operator !=
    def __ne__(self, other:object)->bool:
        other_ = cast(Vector2D,other)
        return not (self._x == other_._x and self._y == other_._y)

    # operator +
    # z : Vector2D
    def __add__(self,z:"Vector2D") -> "Vector2D":
        return Vector2D(self.x + z.x , self.y + z.y)

    # operator +=
    # def __iadd__(self,z:"Vector2D")-> "Vector2D":
    #     self.x += z.x
    #     self.y += z.y
    #     return self
    # → immutableなので実装せず。isub、imulについても同様。

    # operator -
    # z : Vector2D
    def __sub__(self, z:"Vector2D") -> "Vector2D":
        return Vector2D(self.x - z.x , self.y - z.y)

    # operator *
    # z : Vector2D
    def __mul__(self, z:float | int) -> "Vector2D":
        return Vector2D(self.x * z , self.y * z)

    # operator //
    def __floordiv__(self,z:float | int)-> "Vector2D":
        return Vector2D( self.x // z , self.y // z )

    # 文字列化
    def __str__(self):
        return f"({self.x},{self.y})"

    # Vectorを矩形の範囲に収まるようにclampする。
    def clamp(self,rect:"Rect")->"Vector2D":
        return Vector2D(
            MathTools.clamp(self.x, rect.p.x ,rect.p.x + rect.s.x - 1),
            MathTools.clamp(self.y, rect.p.y ,rect.p.y + rect.s.y - 1)
        )

    # 単位ベクトルを返す。
    # kが指定されていれば、そのk倍したものを返す。
    def unit(self,k:float = 1.0)->"Vector2D":
        r = math.sqrt(self.x**2 + self.y**2)
        # ゼロ除算回避
        if r == 0.0:
            return Vector2D(0,0)
        return Vector2D(self.x * k / r , self.y * k / r)

    # このベクトルを座標として見た時に、矩形の範囲内にああるか
    def is_in_rect(self, rect:"Rect") -> bool:
        return  rect.p.x <= self.x < rect.p.x + rect.s.x \
            and rect.p.y <= self.y < rect.p.y + rect.s.y

    # ベクトルのノルム(大きさ)を返す。
    def norm(self)->float:
        return math.sqrt(self.x**2 + self.y**2)

# 矩形領域
class Rect:
    # 矩形領域。
    # p : 左上の座標
    # s : 矩形のサイズ。(width, height)
    def __init__(self,p:Vector2D,s:Vector2D):
        # 左上の座標
        self.p   = p
        # 矩形のサイズ
        self.s   = s
    def __str__(self):
        return f"p={self.p}, s={self.s}"

# ------------------------------------------------------------------------------
#                              文字列操作など
# ------------------------------------------------------------------------------

class StrUtil:
    # 左からn文字切り出す
    @staticmethod
    def left(s:str,n:int):
        return s[:n]

    # 右からn文字切り出す
    @staticmethod
    def right(s:str,n:int):
        return s[-n:]

    # 真ん中n文字目からm文字切り出す
    @staticmethod
    def mid(s:str, n:int, m:int):
        return s[n:n+m]

# ------------------------------------------------------------------------------
#                              キー入力
# ------------------------------------------------------------------------------

# キーコード
class KEY(IntEnum):
    LEFT  = 37
    RIGHT = 39
    UP    = 38
    DOWN  = 40
    SPACE = 32
    ENTER = 13
    # あとで追加する

# キー入力
class KeyInput:
    def __init__(self):

        # キー入力は、DOMの仕様上、document全体を対象とするしかない。(?)
        self.element = document
        
        # 現在押されているキー
        # set() でも良いが、keyCodeは最大でも256までしかないのでそういうテーブルを用意する。
        self._keys      = [False]*256
        # 前回のupdate()の時に押されていたキー
        self._last_keys = [False]*256

        # キーイベントのハンドラの設定
        self.element.addEventListener("keydown", self._key_push)
        self.element.addEventListener("keyup"  , self._key_up)

        # ↑のイベントをremoveした時にTrueになるフラグ
        self._event_removed = False

    # キーが押された時のイベント
    def _key_push(self, e:DOMEvent):
        self._keys[e.keyCode] = True

        # スクロールバーとか動いてしまうの嫌なので抑制
        e.preventDefault()
        e.stopPropagation()

    # キーを離した時のイベント
    def _key_up(self, e:DOMEvent):
        self._keys[e.keyCode] = False
        # スクロールバーとか動いてしまうの嫌なので抑制
        e.preventDefault()
        e.stopPropagation()

    # キーが押されているかを判定して返す。
    def is_key_pressed(self, key:KEY) -> bool:
        return self._keys[key]

    # 何かキーが押されているか？
    def is_any_key_pressed(self) -> bool:
        return any(self._keys)

    # 明示的にeventをremoveする。
    # キー入力がこのクラスに食われてF5キー等が利かなくて困る時に用いる。
    def remove_event(self):
        if not self._event_removed:
            self.element.removeEventListener("keydown", self._key_push)
            self.element.removeEventListener("keyup"  , self._key_up)
            self._event_removed = True

    # コンストラクタでhookしたEventを戻す
    def __del__(self):
        self.remove_event()

# ------------------------------------------------------------------------------
#                              Touchイベント
# ------------------------------------------------------------------------------

# タッチ情報
class TouchInfo:
    # p : 
    def __init__(self, p:"Vector2D" , id:int):
        # タッチされている座標
        self.p = p
        # そのid(タッチ(指)が移動した場合、同一idであることが保証されている)
        self.id = id

# タッチイベント(スマホ等)の入力用
class TouchInput:
    # canvas_id_name : 対象としたいcanvasのid名。Noneを指定すると、document全体。
    def __init__(self , id_name:str="canvas"):

        self.element = document[id_name] if id_name else document
        self.element.addEventListener("touchstart", self._touch_handler)
        self.element.addEventListener("touchmove" , self._touch_handler)
        self.element.addEventListener("touchend"  , self._touch_handler)    

        # 現在押されているリスト
        self.touches:list[TouchInfo] = []
        # 前回の押されていたリスト
        self.last_touches:list[TouchInfo] =[]

    def _touch_handler(self, e:DOMEvent):
        self.touches:list[TouchInfo] = []

        touch_list = e.touches
        for touch in touch_list:
            self.touches.append(TouchInfo(Vector2D(touch.clientX,touch.clientY),touch.identifier))

        # スクロールの防止
        e.preventDefault();

    # 明示的にeventをremoveする。
    # キー入力がこのクラスに食われてF5キー等が利かなくて困る時に用いる。
    def remove_event(self):
        self.element.removeEventListener("touchstart", self._touch_handler)
        self.element.removeEventListener("touchmove" , self._touch_handler)
        self.element.removeEventListener("touchend"  , self._touch_handler)    

    # 現在押されている箇所の一覧を返す。
    def get_info(self)->list[TouchInfo]:
        return self.touches

    # 前回から新規に押されたところだけを返す。
    def get_touchstart_info(self)->list[TouchInfo]:
        touches:list[TouchInfo] = []        
        for touch in self.touches:

            # touch.id が self.last_touches のなかに見つからなければ新規に押されたということなので
            # touchesに追加する。

            found = False
            for last_touch in self.last_touches:
                if touch.id == last_touch.id:
                    found = True
                    break

            if not found:
                touches.append(touch)

        # 保存しておく
        self.last_touches = self.touches
        return touches

    # コンストラクタでhookしたEventを戻す
    def __del__(self):
        self.remove_event()

# マウス情報
class MouseInfo:
    def __init__(self, pos:"Vector2D" , left_button:bool , middle_button:bool , right_button:bool):

        # 座標(x,y) 対象とするelementの左上を原点とする。
        self.p = pos

        # 各ボタンの状態
        self.left_button   = left_button
        self.middle_button = middle_button
        self.right_button  = right_button

    def clone(self)->"MouseInfo":
        return MouseInfo(self.p, self.left_button, self.middle_button, self.right_button)

    def __str__(self)->str:
        return f"{self.p} , L={self.left_button}, M={self.middle_button}, R={self.right_button}"

# マウス入力
class MouseInput:
    # canvas_id_name : 対象としたいcanvasのid名。Noneを指定すると、document全体。
    def __init__(self , id_name:str="canvas"):
        self.element = document[id_name] if id_name else document
        self.element.addEventListener("mousemove"   , self._mouse_move  )
        self.element.addEventListener("mousedown"   , self._mouse_updown)
        self.element.addEventListener("mouseup"     , self._mouse_updown)
        self.element.addEventListener("contextmenu" , self._contextmenu )

        # マウスの現在の状態(次のframeまでに書き換わるので、そのあと書き換わって困るなら、clone()して用いること。)
        self.info      = MouseInfo(Vector2D(-99999,-99999), False,False,False)

    # マウスの現在の状態(次のframeまでに書き換わるので、そのあと書き換わって困るなら、clone()して用いること。)
    def get_info(self)->MouseInfo:
        return self.info

    # マウスの移動ハンドラ
    def _mouse_move(self, e:DOMEvent):
        self.info.p = Vector2D(e.offsetX, e.offsetY)

    # マウスのボタン押し下げハンドラ
    def _mouse_updown(self, e:DOMEvent):
        self.info.left_button   = bool(e.buttons & 1)
        self.info.right_button  = bool(e.buttons & 2)
        self.info.middle_button = bool(e.buttons & 4)

    def _contextmenu(self, e:DOMEvent):
        # コンテキストメニューの出現をキャンセル
        e.preventDefault();
        
    # 明示的にeventをremoveする。
    # キー入力がこのクラスに食われてF5キー等が利かなくて困る時に用いる。
    def remove_event(self):
        self.element.removeEventListener("mousemove"   , self._mouse_move  )
        self.element.removeEventListener("mousedown"   , self._mouse_updown)
        self.element.removeEventListener("mouseup"     , self._mouse_updown)
        self.element.removeEventListener("contextmenu" , self._contextmenu )

    # コンストラクタでhookしたEventを戻す
    def __del__(self):
        self.remove_event()

# 仮想キー(VirtualKeyInputを使う時に使えるかも)
class VKEY(IntEnum):
    SPACE = 0
    ENTER = 1
    LEFT  = 2
    RIGHT = 3
    DOWN  = 4
    UP    = 5
    # あとで追加するかも

# 仮想キー入力
# スペースキー、マウスクリック(右 or 左)、画面タッチ(スマホ)のいずれでもスペースキーが押されたとみなす、みたいな感じのことができる。
# 使い方)
#  register_handler()でハンドラを登録するか、configure_1key_game()のようなconfigureを自動でやってくれる関数を呼び出す。
#  以降は、1 frameごとにupdate()を呼び出し、そのあと is_key_pressed() / is_key_pushed() で、
#  ある仮想キーが押されているか/押し下げられたかを判定できる。
class VirtualKeyInput:

    # id_name : キー入力の対象とするHTML element。document全体にするならNoneを指定。
    def __init__(self, id_name : str = "canvas"):
        self.key_input = KeyInput()
        self.touch_input = TouchInput(id_name)
        self.mouse_input = MouseInput(id_name)

        # update()が呼び出された時に呼び出されるハンドラ。
        # 仮想キーごとにハンドラを用意すると、touch_inputに対するハンドラが書きにくくて良くない設計。
        self.handler:Callable[[],None] | None = None

        # 前回と今回、それぞれのキーが押されていたかの情報。update()呼び出しごとに更新される。
        self._key_pressed_previous:list[bool] = []
        self. key_pressed_current :list[bool] = [False]*16 # 最大 16key

        # update()のあと、(有効矩形内で)タッチされていた箇所。なければNone。configure_6keys_8directions_game()などを用いる時のみ有効。
        self.touch_pos:Vector2D | None = None

    # ワンキーゲーム用のお手軽設定
    # 仮想キー VKEY.SPACE として以下のように設定する。
    #   key   : Space、Enter
    #   mouse : 左・右ボタン
    #   touch : 画面タッチ
    def configure_1key_game(self):
        def handler():
            mouse = self.mouse_input.get_info()
            self.key_pressed_current[VKEY.SPACE] = \
                self.key_input.is_key_pressed(KEY.SPACE) or self.key_input.is_key_pressed(KEY.ENTER) or \
                mouse.left_button or mouse.right_button or \
                len(self.touch_input.get_info()) > 0 

        self.register_handler(handler)

    # 左右キーのみのゲーム用のお手軽設定
    # ※　あくまで書き方のサンプル。この仕様が気にいらなければ、この関数をコピペして書き換えてregister_handler()を呼び出すと良いと思う。
    # 仮想キー VKEY.LEFT として以下のように設定する。
    #   key   : 左カーソル
    #   mouse : 左ボタン
    #   touch : 画面左半分のタッチ
    # 仮想キー VKEY.RIGHT として以下のように設定する。
    #   key   : 右カーソル
    #   mouse : 右ボタン
    #   touch : 画面右半分のタッチ
    # 仮想キー VKEY.SPACE , VKEY.ENTER として以下のように設定する。
    #   key   : SPACE , Enter
    #
    # r0 : タッチされた時に 仮想キー0としてみなす矩形領域(デフォルトでは400px × 400px のcanvasの左半分)
    # r1 : タッチされた時に 仮想キー1としてみなす矩形領域(デフォルトでは400px × 400px のcanvasの右半分)
    def configure_4keys_2directions_game(self, r0:Rect=Rect(Vector2D(0,0),Vector2D(200,400)), r1:Rect=Rect(Vector2D(200,0),Vector2D(200,400))):

        def handler():
            mouse = self.mouse_input.get_info()
            self.key_pressed_current[VKEY.LEFT ] = self.key_input.is_key_pressed(KEY.LEFT ) or\
                    mouse.left_button or \
                    (len(self.touch_input.get_info()) > 0 and self.touch_input.get_info()[0].p.is_in_rect(r0))

            self.key_pressed_current[VKEY.RIGHT] = self.key_input.is_key_pressed(KEY.RIGHT) or\
                    mouse.right_button or \
                    (len(self.touch_input.get_info()) > 0 and self.touch_input.get_info()[0].p.is_in_rect(r1))

            self.key_pressed_current[VKEY.SPACE] = self.key_input.is_key_pressed(KEY.SPACE)
            self.key_pressed_current[VKEY.ENTER] = self.key_input.is_key_pressed(KEY.ENTER)

        self.register_handler(handler)

    # 上下左右キーのみのゲーム用のお手軽設定。斜め入力は無しの場合について。(ありの場合はconfigure_6keys_8directions_game()を呼び出すこと。)
    # ※　あくまで書き方のサンプル。この仕様が気にいらなければ、この関数をコピペして書き換えてregister_handler()を呼び出すと良いと思う。
    # 仮想キー VKEY.LEFTとして以下のように設定する。
    #   key   : 左カーソル
    #   mouse , touch : 指定した矩形の左らへんのタッチ
    # 仮想キー VKEY.RIGHTとして以下のように設定する。
    #   key   : 右カーソル
    #   mouse , touch : 指定した矩形の右らへんのタッチ
    # 仮想キー VKEY.DOWNとして以下のように設定する。
    #   key   : 下カーソル
    #   mouse , touch : 指定した矩形の下らへんのタッチ
    # 仮想キー VKEY.UPとして以下のように設定する。
    #   key   : 上カーソル
    #   mouse , touch : 指定した矩形の上らへんのタッチ
    # 仮想キー VKEY.SPACE として以下のように設定する。
    #   key   : Space
    #   mouse : 左クリック
    #   touch : 任意箇所
    # 仮想キー VKEY.ENTER として以下のように設定する。
    #   key   : Enter
    # 
    #  r      : マウスクリック、タッチの有効矩形。このなかだけ有効。
    # タッチされた箇所は、self.touch_posに反映される。
    def configure_6keys_4directions_game(self, r:Rect=Rect(Vector2D(0,0),Vector2D(200,200))):
        self.register_handler(lambda : self._6keys_handler(r, 45))

    # 上下左右キーのみのゲーム用のお手軽設定。斜め入力もありうる場合について。(なしの場合はconfigure_6directios_game()を呼び出すこと。)
    # その他は、configure_6keys_4directios_gameと同じ。
    def configure_6keys_8directions_game(self, r:Rect=Rect(Vector2D(0,0),Vector2D(200,200))):
        self.register_handler(lambda : self._6keys_handler(r, 45))

    # ↑で使うhandler
    # r              : マウスクリック、タッチの有効矩形。このなかだけ有効。
    def _6keys_handler(self, r:Rect, tolerance:float)->None:
        mouse = self.mouse_input.get_info()

        # キー入力
        self.key_pressed_current[VKEY.SPACE] = self.key_input.is_key_pressed(KEY.SPACE) or \
                mouse.left_button or \
                len(self.touch_input.get_info()) > 0
                # 仮想キー VEKY.SPACEに、これらを入れておかないと is_any_key_pressed()で開始待ちをしている時に画面タッチしてもゲームが始まらない。

        self.key_pressed_current[VKEY.ENTER] = self.key_input.is_key_pressed(KEY.ENTER)

        self.key_pressed_current[VKEY.LEFT ] = self.key_input.is_key_pressed(KEY.LEFT )
        self.key_pressed_current[VKEY.RIGHT] = self.key_input.is_key_pressed(KEY.RIGHT)
        self.key_pressed_current[VKEY.DOWN ] = self.key_input.is_key_pressed(KEY.DOWN )
        self.key_pressed_current[VKEY.UP   ] = self.key_input.is_key_pressed(KEY.UP   )
                
        # マウスか、タッチで矩形内のものを探す。マウスは、左クリックされていなければ無視。
        p:Vector2D | None = None
        if mouse.left_button and mouse.p.is_in_rect(r):
            p = mouse.p
        else:
            # マウスは矩形内になかったのでタッチを調べる。
            touch_list = self.touch_input.get_info()
            for touch in touch_list:
                if touch.p.is_in_rect(r):
                    # 矩形内にあった。
                    p = touch.p
                    break

        # タッチされていた。
        if p:
            # rect中心からどの方角なのか
            d = p - (r.p + r.s//2)
            if d.norm() <= 5:
                # 矩形中心から小さすぎる距離なのでニュートラル(レバーが中央のままで、入力なし)扱い。
                p = None
            else:
                # ベクトルの角度を0-360で返す。
                deg = MathTools.atan_deg(d)

                # 4方向を考える。例えば、右上なら 45°方向。右下なら -45°(270+45)方向。
                # 
                # このとき、上としてみなしたいのは、90°±45°。
                # ゆえに、45° <= deg <= 180°-45° には、"上"方向の成分の入力があると考えられる。
                # 以下、同様。ゆえに以下の式でtolerance = 45。

                # 8方向を考える場合。
                # 
                # このとき、右上としてみなしたいのは、45°±22.5°。
                # 　　　　　左上としてみなしたいのは、90+45±22.5°。
                # ゆえに、22.5° <= deg <= 180°-22.5° には、"上"方向の成分の入力があると考えられる。
                # 以下、同様。ゆえに以下の式でtolerance = 22.5。

                if  90 + tolerance <= deg <= 270 - tolerance:       # 左方向
                    self.key_pressed_current[VKEY.LEFT ] = True
                if deg <= 90 - tolerance or 270 + tolerance <= deg: # 右方向
                    self.key_pressed_current[VKEY.RIGHT] = True
                if 180 + tolerance <= deg <= 360 - tolerance:       # 下方向
                    self.key_pressed_current[VKEY.DOWN ] = True
                if   0 + tolerance <= deg <= 180 - tolerance:       # 上方向
                    self.key_pressed_current[VKEY.UP   ] = True
                
        self.touch_pos = p


    # update()の時に呼び出されるハンドラを登録する。
    # このハンドラは、
    #  1. self.key_pressed_currentを更新しなければならない。
    #  2. 登録する時に self.key_pressed_currentを仮想キーの数だけ確保しなくてはならない。
    def register_handler(self,handler:Callable[[],None]):
        self.handler = handler

    # 仮想キーが押されたかを返す。
    # key : 仮想キー番号(0から register_handler()を呼び出した回数 - 1 まで)
    def is_key_pressed(self,key:VKEY):
        # 登録されているハンドラを呼び出すだけ。
        return self.key_pressed_current[key]

    # いずれかの仮想キーが押されていたらTrueを返す。
    def is_any_key_pressed(self):
        return any(self.key_pressed_current)

    # 仮想キーが(前回のupdate呼び出し時は押されていなくて)新規に押されたのかを返す。
    # そのframeでまずupdate()を一度呼び出して、そのあと、各仮想キーに対してこのメソッドを呼び出していく。
    # 例)
    #  keyinput.update()
    #  if keyinput.is_key_pushed(0):
    #    ...
    def is_key_pushed(self,key:VKEY):

        if len(self._key_pressed_previous) != len(self.key_pressed_current):
            # update()を呼び忘れている。
            raise Exception("please call VirtualKeyInput.update()")

        # 前回押されていなくて、今回押されている。
        return not self._key_pressed_previous[key] and self.key_pressed_current[key]

    # is_key_pushed()を使いたいなら、この関数を1 frameごとに呼び出すこと。
    def update(self):
        # 前回の情報を退避させる。
        self._key_pressed_previous = self.key_pressed_current.copy()
        
        # ハンドラを呼び出す。
        # (このハンドラが self.key_pressed_currentを更新してくれる。)
        if self.handler:
            self.handler()

    # 明示的にeventをremoveする。
    # キー入力がこのクラスに食われてF5キー等が利かなくて困る時に用いる。
    def remove_event(self):
        self.key_input  .remove_event()
        self.touch_input.remove_event()
        self.mouse_input.remove_event()
        
    # コンストラクタでhookしたEventを戻す
    def __del__(self):
        self.remove_event()

# ------------------------------------------------------------------------------
#                              音声・Multimedia
# ------------------------------------------------------------------------------

# 音声用class
class Audio:
    # sound_filename : 音声ファイル("audios"フォルダに配置してあるものとする)
    def __init__(self, audio_filename:str):
        path = "audios\\" + audio_filename
        audio = document.createElement("audio")
        audio["src"] = path
        self.audio = audio

        # unlock()が呼び出されたかのフラグ
        self.unlocked = False

    # 再生する。
    #    sound = Sound("se.wav")
    #    document.body.bind("mousemove", lambda ev : sound.play() )
    # のようにユーザーがアクションを行った時のイベントハンドラでしか再生されない。
    # 現在、ほとんどのブラウザがそういうポリシーに変更されてしまったようだ。
    # なので、以下のUnlockAudio()と組み合わせて使う。
    def play(self):
        if not self.unlocked:
            return
        self.audio.currentTime = 0
        self.audio.play()

    # 停止する。
    def stop(self):
        if not self.unlocked:
            return
        self.audio.stop()

    # 使える状態にする。ユーザーのタップイベントなどでまとめてunlockしておくと良い。
    # cf. JavaScript で音声再生まとめ (marmooo's blog) : https://marmooo.blogspot.com/2021/06/javascript.html
    def unlock(self):
        self.unlocked = True
        self.audio.volume = 0
        self.audio.play()
        self.audio.pause()
        self.currentTime = 0
        self.audio.volume = 1

# audioを管理してくれる。
class AudioLoader:
    # hookするevent
    # keydownは、KeyInputのハンドラが
    #    e.preventDefault()
    #    e.stopPropagation()
    # としているが、前者は、FORMのsubmitみたいな動作をキャンセルするだけだし、後者は親要素への伝播を停止するだけなので、
    # ここでのkeydownが呼び出されなくなるわけではないのでセーフ。
    event_names:list[str] = ["touchstart", "keydown" , "mousedown"]

    # 使いたいaudioファイルの一覧を渡す。
    def __init__(self , audio_filenames:list[str]):

        # ↓ここに読み込まれる。
        self.audios:list[Audio] = []
        for filename in audio_filenames:
            self.audios.append(Audio(filename))

        self._unlocked = False
        self._add_events()

    def _add_events(self):
        for event_name in AudioLoader.event_names:
            document.addEventListener(event_name, self._event_handler )
        
    def _remove_events(self):
        # 一度だけ呼び出されればOKなのでイベントハンドラの登録を解除しておく。
        for event_name in AudioLoader.event_names:
            document.removeEventListener(event_name, self._event_handler )

    def _event_handler(self, evt:DOMEvent):
        self._unlock_audios()
        self._remove_events()

    # Audioをunlockして良いタイミングで呼び出す。(ユーザーのキーイベントなど)
    def _unlock_audios(self):
        if self._unlocked:
            return # タイミングのずれで二度呼び出されることがある

        for audio in self.audios:
            audio.unlock()

        self._unlocked = True

# ------------------------------------------------------------------------------
#                              画面・画像
# ------------------------------------------------------------------------------

# 画像用class
class Image:
    # image_filename : 画像ファイル名("images"フォルダに配置してあるものとする)
    # ここで読み込んだ画像は、Canvas.draw_image()などで描画できる。
    def __init__(self, image_filename:str):
        self.image = window.Image.new()
        # self.image.src = image_filename と書くとwarningが出る。
        self.image["src"] = "images\\" + image_filename

    # 画像サイズ
    # self.size = Vector2D(self.image.naturalWidth , self.image.naturalHeight)
    # →　このタイミングだと画像読み込みが完了していないため、(0,0)になってしまう。
    def get_size(self)->"Vector2D":
        return Vector2D(self.image.naturalWidth , self.image.naturalHeight)

    # 画像が読み込み完了しているかを返す。
    def load_completed(self)->bool:
        # 読み込みが完了しているなら画像の幅が得られているはず。
        return self.image.naturalWidth != 0

# 画像を管理してくれる。
class ImageLoader:
    # 使いたい画像ファイルの一覧を渡す。
    def __init__(self , image_filenames:list[str]):

        # ↓ここに読み込まれる。
        self.images:list[Image] = []

        for filename in image_filenames:
            self.images.append(Image(filename))

    # 読み込みが完了している画像の数を返す
    def completed_num(self)->int:
        # generator式で書くと短く書ける。
        return sum((image.load_completed() for image in self.images))

    # すべての画像の読み込みが完了しているのか。していればTrueが返る。
    def load_completed(self)->bool:
        return self.completed_num() == len(self.images)


# 描画用canvas
class Canvas:
    # canvas_id_name : HTML5のcanvasにつけたid名。defaultでは"canvas"
    def __init__(self, canvas_id_name:str = "canvas"):
        # 描画するcanvasのcontextの取得。
        # wrapper要素の縦横を取得して、self.canvasもそれに合致させることで文字のぼやけを防ぐ
        self.canvas = document[canvas_id_name]
        self.wrapper = document['wrapper']
        self.ctx = self.canvas.getContext("2d")

        # debug
        # print('キャンバスの要素')
        # for key, value in self.canvas.__dict__.items():
        #     print(key, ':', value)
        # print('wrapperの要素')
        # for key, value in self.wrapper.__dict__.items():
        #     print(key, ':', value)

        # 画面いっぱいにcanvasを合わせる
        # スマホ、PCどちらでも同じレイアウト
        self.canvas.attrs['width'] = self.wrapper.clientWidth
        self.canvas.attrs['height'] = self.wrapper.clientHeight
        self.width:int = self.canvas.width
        self.height:int = self.canvas.height

        # 文字のぼやけ解消のためパーセンテージ調整
        # self.width :int = int(self.width*0.5)
        # self.height:int = int(self.height*0.5)
        
        # canvasのRect
        self.rect = Rect(
            Vector2D(0,0) ,
            Vector2D(self.width, self.height)
        )

    # 画面のクリア
    # 任意の色で初期化したい時はcolorに好きな色を入れる
    def clear(self, color:str="black"):
        # canvas丸ごと塗りつぶし
        self.draw_rect(self.rect.p , self.rect.s, color)

    # 矩形の描画(塗りつぶし)
    # p  : 左上の座標 ( left  ,   top )
    # s  : 矩形サイズ ( width , height)
    def draw_rect(self, p:Vector2D, s:Vector2D, color:str="black"):
        self.ctx.fillStyle = color
        self.ctx.fillRect(p.x, p.y, s.x, s.y)

    # 矩形の描画(指定した座標に矩形の中央が来るように描画)
    # colorは make_color()を使ってRGBで指定することもできる。
    # ("red","blue"のような文字列と"#808080"のような16進数RGB文字列が使える)
    def draw_rect_center(self, p:Vector2D, s:Vector2D, color:str="black"):
        self.draw_rect(p - s//2 , s , color)

    # 矩形の線だけの描画
    # p  : 左上の座標 ( left  ,   top )
    # s  : 矩形サイズ ( width , height)
    def draw_rectline(self, p:Vector2D, s: Vector2D, color:str="black"):
        self.ctx.strokeStyle = color
        self.ctx.strokeRect(p.x, p.y, s.x, s.y);        

    # Imageクラスの描画
    # p       : 描画したい座標
    # srcPos  : 転送元画像の転送したい矩形の左上の座標(Noneを指定すれば (0,0) を指定したのと同じ)
    # srcSize : 転送元画像の転送したい矩形の大きさ    (Noneを指定すれば転送元の画像全体と同じ大きさ)
    # dstSize : 描画先での大きさ                    (Noneを指定すれば転送元と同じ)
    def draw_image(self,image:Image, p:Vector2D ,\
         srcPos:Vector2D = Vector2D(0,0) , srcSize:Vector2D | None = None,
         dstSize:Vector2D | None =None ):

        # 読み込みが完了していなければ(失敗しているなどでも) width == 0 なので
        # その状態なら、描画をskipする。
        if not image.load_completed():
            return 
        if not srcSize: # srcSizeが指定されていなければ、転送元画像のサイズそのまま
            srcSize = image.get_size()
        if not dstSize: # dstSizeが指定されていなければ、転送元のサイズと同じ(等倍)
            dstSize = srcSize

        self.ctx.drawImage(image.image, srcPos.x , srcPos.y, \
            srcSize.x , srcSize.y , p.x, p.y , dstSize.x, dstSize.y )

    # Imageクラスを描画(指定した座標に画像の中央が来るように描画)
    # p       : 描画したい座標
    # srcPos  : 転送元画像の転送したい矩形の左上の座標(Noneを指定すれば (0,0) を指定したのと同じ)
    # srcSize : 転送元画像の転送したい矩形の大きさ    (Noneを指定すれば転送元の画像全体と同じ大きさ)
    # dstSize : 描画先での大きさ                    (Noneを指定すれば転送元と同じ)
    def draw_image_center(self, image:Image, p:Vector2D, \
         srcPos:Vector2D = Vector2D(0,0) , srcSize:Vector2D | None = None,
         dstSize:Vector2D | None =None ):

        if not srcSize: # srcSizeが指定されていなければ、転送元画像のサイズそのまま
            srcSize = image.get_size()
        if not dstSize: # dstSizeが指定されていなければ、転送元のサイズと同じ(等倍)
            dstSize = srcSize

        self.draw_image(image , p - dstSize // 2 ,\
             srcPos = srcPos , srcSize = srcSize , dstSize = dstSize)

    # 文字をcanvasに描画
    # p : 文字列の左上の座標
    # colorは make_color()を使ってRGBで指定することもできる。
    # ("red","blue"のような文字列と"#808080"のような16進数RGB文字列が使える)
    def draw_text(self, text:str, p:Vector2D, font:str="32px serif",color:str="white"):
        self.ctx.font = font
        self.ctx.fillStyle = color
        self.ctx.textBaseline = "top"
        self.ctx.fillText(text, p.x, p.y)

    # 文字をcanvasに描画
    # draw_textの中央揃え版。
    # p : 文字列の中央にしたい座標。
    def draw_text_center(self, text:str, p:Vector2D, font:str="32px serif",color:str="white"):
        self.ctx.font = font
        self.ctx.fillStyle = color
        self.ctx.textBaseline = "top"

        # 描画される幅を計測する
        textWidth:int = self.ctx.measureText(text).width

        # その幅の分だけ左側から表示。
        self.ctx.fillText(text, p.x - textWidth//2, p.y)

    # RGB値からCSSで使う文字列を作る。
    # r,g,b : 0-255の範囲
    # r=g=b=128なら"#808080"という文字が返る。
    @staticmethod
    def make_color(r:int,g:int,b:int)->str:
        # 2文字の16進数にする。
        def toHex(x:int):
            return ('0' + format(x,"x"))[-2:]
        return f"#{toHex(r)}{toHex(g)}{toHex(b)}"

    # message dialogを出す。
    @staticmethod
    def message_dialog(text:str):
        Dialog(text , ok_cancel=True)

# ------------------------------------------------------------------------------
#                              Timerなど
# ------------------------------------------------------------------------------

# ゲーム用の描画ループ
class GameTimer:
    def __init__(self , onDrawFunction:Callable[[],None] | None = None, fps:int=15):

        self._game_loop = None

        # 描画関数が設定されていれば、即座にstartさせる
        if onDrawFunction:
            self.start(onDrawFunction,fps = fps)

    # 描画する関数を登録する。
    # fps : 1秒間のフレーム数
    # onDrawFunction : 1フレームごとに呼び出す描画用の関数
    def start(self, onDrawFunction:Callable[[],None],fps:int | float=15):

        # 以前にstart()が呼び出されていたのなら、それを停止させる。
        self.stop()

        # ゲーム用のループ。例外が出たらそのメッセージとトレースバックを表示
        def gameloop():
            try:
                onDrawFunction()
            except Exception:
                InfoDialog("Exception",traceback.format_exc())
                self.stop()

        # 描画する関数onDrawを定期的に呼び出す
        self._game_loop = window.setInterval(gameloop, 1000 / fps)  # 15 FPS

    # start()で開始させたゲームを終了させる。
    # from_start : start()から呼び出された時にTrueになる。
    def stop(self):
        if self._game_loop:
            window.clearInterval(self._game_loop)
            self._game_loop = None

# 経過時間の計測用
class ElapsedTimer:
    def __init__(self):
        self.reset()

    # タイマーをリセットする。
    # elapsed()を呼び出した時に、reset()からの経過時間が返る。
    # コンストラクタでもreset()を呼び出しているので、コンストラクタ生成からの経過時間が知りたいなら、
    # このreset()を呼び出す必要はない。
    def reset(self):
        # start_time : resetを呼び出してからの経過時間
        self.start_time = self.now()

    # 経過時間が返る。単位は秒。float型なので0.5秒なら0.5。
    def elapsed(self)->float:
        return self.now() - self.start_time

    # 現在の時刻を返す。何かからの経過時間。単位は秒。
    def now(self)->float:
        return timer() # timeit

# ------------------------------------------------------------------------------
#                              GameObject
# ------------------------------------------------------------------------------

# GameObjectのOnDraw()で渡すパラメーターの基底class。これから派生させる。
class GameContext:
    pass

# ゲームに出てくる物体
class GameObject:
    # p : Vector2D , 座標
    def __init__(self):

        # オブジェクトの削除マーク
        # (これがTrueだと、次のフレームで削除される)
        self.deleted = False

    # 描画に対して呼び出される。派生クラス側でoverrideする。
    # contextは、描画に必要なためのクラスを指定する。
    def onDraw(self,context:GameContext):
        pass

# GameObjectを追加したり削除したりする。
class GameObjectManager(GameObject):
    def __init__(self):
        # ゲーム上の物体
        self.objects:list[GameObject] = []

    # このclassをiterableにしておく。
    # def __iter__(self):
    #     # yield from self.objects
    #     # →　途中でappend()される可能性を考慮して以下のように書く。     
    #     i = 0
    #     while i < len(self.objects):
    #         yield self.objects[i]
    #         i += 1
    # →　わかりにくいので素直に self.objects 使ったほうがいいと思う。

    # GameObjectを追加する。
    def append(self,object:GameObject):
        self.objects.append(object)

    # このクラスの持つ objects(GameObjectのlist)に対してonDraw()を呼び出してやる。
    # onDraw()のなかで このクラスのappend()が呼び出されてもうまく動くようになっている。
    def onDraw(self,context:GameContext):

        # ゲームオブジェクトの描画
        # onDrawのなかで追加されることがあるのでappendに対して安全にしておく必要がある。
        # また、このframeで追加されたものに対してonDraw()を呼び出すことを保証したい。
        # なので通常のforループでは書けない。

        i = 0
        while i < len(self.objects):
            self.objects[i].onDraw(context)
            i += 1

        # 備考) listに対してforで回している時のappend、Pythonでは現状問題がないようだ。
        #       しかし今後、変わる恐れがあるのでこの仕様に依存した書き方をしない。
        #       https://dev.classmethod.jp/articles/python-delete-element-of-list/

        # deleteフラグが立っているものはremoveする。
        self.objects = [obj for obj in self.objects if not obj.deleted]
