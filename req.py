import json
import random
import bisect
from array import array

def get_url(send_url,params="None"):
    from browser import document, ajax

    #paramsが設定されていた場合に実行(パラメータをセット)
    if params != "None":
        send_url = send_url + "?isbn=" + params

    # send a POST request to the url
    # Bind the complete State to the on_get_complete function
    req = ajax.Ajax()
    req.open('GET', send_url, False)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send()
    return req

# すべてのISBNを取得
res = get_url('https://api.openbd.jp/v1/coverage')
seq = json.loads(res.text)

# isbnが9784からはじまるものだけにする
seq = seq[bisect.bisect_left(seq,'9784000000000'):bisect.bisect_right(seq,'9784999999999')]

# ランダムに500冊を選んでjsonを取得
ranseq = random.sample(seq, 500)

# 書籍情報の取得
res = get_url('https://api.openbd.jp/v1/get', params='%2C'.join(ranseq))
seq = json.loads(res.text)

# titleを取得
titles = array('u',[r["onix"]["DescriptiveDetail"]["TitleDetail"]["TitleElement"]["TitleText"].get("content") for r in seq])
# print(titles)
# 使わない変数を削除してメモリを確保
del seq,res,ranseq
