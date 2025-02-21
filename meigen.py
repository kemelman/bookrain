import random
say={
    '良い本は私の人生におけるイベントである。': 'スタンダール（フランスの小説家／1783－1842）',
    '本の無い家は窓の無い部屋のようなものだ。': 'ハインリヒ・マン（ドイツの作家／1871－1950）',
    '読もうとしない人は読めない人に劣る。': 'マーク・トウェイン（アメリカの小説家／1835－1910）',
    '本の無い部屋は魂の無い身体のようなものだ。': 'マルクス・トゥッリウス・キケロ（古代ローマの政治家／紀元前106－紀元前43）',
    '作家は本を始めるだけである。読者が本を終わらせる。': 'サミュエル・ジョンソン（イギリスの文学者／1709－1784）',
    '古典とは、人々は称賛するが読まない本のことである。': 'マーク・トウェイン（アメリカの小説家／1835－1910）',
    '膨大な量の本があるにもかかわらず、読む人のなんと少ないことか！': 'ヴォルテール（フランスの哲学者／1694－1778）',
    '私は、自分がこれまでに読んだあらゆるものの一部である。': 'セオドア・ルーズベルト（アメリカの元大統領／1858－1919）',
    '今日読める本を明日まで延ばしてはならない。': 'ホルブルック・ジャクソン（イギリスのジャーナリスト／1874－1948）',
    '読書ほど安い娯楽も、長続きする喜びもない。': 'メアリー・ウォートリー・モンタギュー（イギリスの著述家／1689－1762）',
    '読書は私たちに未知の友人をもたらす。': 'オノレ・ド・バルザック（フランスの小説家／1799－1850）',
    '読書は、自分の頭ではなく他人の頭で考えるのと同じである。': 'アルトゥル・ショーペンハウアー（ドイツの哲学者／1788－1860）',
    '心にとっての読書は、身体にとっての運動と同じである。': 'リチャード・スティール（アイルランドの作家／1672－1729）',
    '最高の本とは、あなたが既に知っていることを教えてくれるものである。': 'ジョージ・オーウェル（イギリスの作家／1903－1950）',
    'あなたが絶対に知るべき唯一のものとは、図書館の場所である。': 'アルベルト・アインシュタイン（ドイツ生まれの物理学者／1879－1955）',
    'あらゆる良書を読むことは、過去数世紀の最高の人々と会話するようなものだ。': 'デカルト（フランスの哲学者／1596－1650）',
    '反省せずに読むことは、消化せずに食べるようなものだ。': 'エドマンド・バーク（アイルランド生まれの哲学者／1729－1797）',
    '今日の読書家は明日のリーダーである。': 'マーガレット・フラー（アメリカのジャーナリスト／1810－1850）',
    '書物の新しいページを1ページ、1ページ読むごとに、私はより豊かに、より強く、より高くなっていく。':'アントン・チェーホフ（ロシアの劇作家、小説家／1860－1904）',
    '今日の読書こそ、真の学問である。':'吉田松陰（幕末の長州藩士／1830－1859）',
    '私が人生を知ったのは、人と接したからではなく、本と接したからである。':'アナトール・フランス（フランスの詩人、小説家／1844－1924）',
    '読書を廃す、これ自殺なり。':'国木田独歩（日本の小説家、詩人／1871－1908）',
    '私は本がなければ生きられない。':'トーマス・ジェファーソン（アメリカの元大統領／1743－1826）',
    'たった一冊の本しか読んだことのない者を警戒せよ。':'ベンジャミン・ディズレーリ（イギリスの政治家、小説家／1804－1881）',
    '書物は我々のうちなる凍った海のための斧なのだ。':'フランツ・カフカ（現在のチェコ出身の小説家／1883－1924）',
    '他人の自我にたえず耳を貸さねばならぬこと、それこそまさに読書ということなのだ。':'ニーチェ（ドイツの哲学者、思想家／1844－1900）',
    '読書家の一族は、世界を動かす者たちなのだ。':'ナポレオン・ボナパルト（フランスの軍人、政治家／1769－1821）',
    '一時間の読書をもってしても和らげることのできない悩みの種に、私はお目にかかったことがない。':'シャルル・ド・モンテスキュー（フランスの哲学者／1689－1755）',
    '本をよく読むことで自分を成長させていきなさい。本は著者がとても苦労して身に付けたことを、たやすく手に入れさせてくれるのだ。':'ソクラテス（古代ギリシアの哲学者／紀元前469－紀元前399）',
    '良書を初めて読むときは、新しい友を得たようである。前に精読した書物を読みなおす時は、旧友に会うのと似ている。':'オリヴァー・ゴールドスミス（イギリスの詩人、小説家／1728－1774）',
    '文芸の第一の利益は人生を知ることにある。人間生活の真相を知ることにある。': '菊池寛（小説家、劇作家、ジャーナリスト／1888－1948）',
    '読むのを学ぶことは火を付けることである。綴られた全ての音節が火花である。': 'ヴィクトル・ユーゴー（フランスの詩人／1802－1885）',
    '本を読むことを止めることは、思索することを止めることである。': 'フョードル・ドストエフスキー（ロシアの小説家、思想家／1821－1881）',
    '少しの隙あらば、物の本を、文字のある物を懐に入れ、常に人目を忍び、見るべし。': '北条早雲（戦国時代初期の武将／1456－1519）',
}
told, author = random.choice(list(say.items()))
