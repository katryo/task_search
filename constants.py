# -*- coding: utf-8 -*-
THRESHOLD_FOR_REMOVING_FROM_PART_OF = 2.0
THRESHOLD_FOR_UNITING_IN_PART_OF = 0.4
THRESHOLD_FOR_FREQUENTLY_APPERING_TASK = 0.5
DEFAULT_DISTANCE_BETWEEN_TASK_AND_SUBTYPE = 1000
THRESHOLD_DISTANCE_FOR_REMOVING_FROM_PART_OF = 50  # part-ofで使う
NUM_OF_PAGE_PER_QUERY = 100

SUPERTYPE_NAME = 'SUPERTYPE'
FETCHED_PAGES_DIR_NAME = 'fetched_pages'
FETCHED_PAGES_WITH_TASK_FOR_EX_DIR_NAME = 'fetched_pages_with_task_for_expanded_queries'
FETCHED_PAGES_O_DIR_NAME = 'fetched_pages_for_original_queries'
FETCHED_ADS_DIR_NAME = 'fetched_ads'
QUERIES_DIR_NAME = 'queries'
ANSWERER_DIR_NAME = 'answerers'
GRAPH_DIR_NAME = 'graphs'
ENTAILMENT_DICTIONARIES_DIR_NAME = 'entailment_dictionaries'
# ENTAILMENT_DICTIONARY_NAMES = 'ent_presu ent_triv nonent_predi ent_ntriv nonent_ntriv'.split(' ')
ENTAILMENT_DICTIONARY_TABLENAMES = 'entailment_acrac entailment_ntriv entailment_presu entailment_triv nonentailment_anton nonentailment_ntriv nonentailment_predi nonentailment_triv'.split(' ')
STOPWORDS_OF_HYPOHYPE = 'ドラマ 作品 舞台 番組 出演作品 ' \
                        '映画 短編 登場 キャラクター 掲載作家 ' \
                        '投稿戦士 現在所属 敵以外 人物 種類 ジャンル ' \
                        '小説 書籍 詩集 漫画 アイヌ語 ' \
                        '劇中 に関する にある ' \
                        '麻雀用語 和製漢語 ' \
                        '歌謡曲 主題歌 楽曲 収録曲 アルバム CD・曲 ' \
                        'ソング シングル 収録曲 '.split(' ')
STOPWORDS_OF_SUBTYPES = 'の部屋 の国'.split(' ')
STOPWORDS_OF_WEBPAGE_NOUN = '是非 どこ だけ ごちゃごちゃ ： : について 方 コメント ' \
                            'お気に入り お気に入り詳細 リンク レス 注意事項 よくある質問コンテンツ よくある質問 ' \
                            'FAQ ＦＡＱ 有効 機能 ファイル 方法 まで 何 メールフォーム ' \
                            '自己責任 JavaScriptの設定方法 知恵コレクション コメント コメント投稿' \
                            'goo メールアドレス サイト画像 ｗｅｂサイト webサイト ' \
                            '当店 ボタン ブラウザ ブラウザー ポイント メッセージ ファイル名 ' \
                            '画面 参考 お客様の声 ページ サイト カート どんどんカート ' \
                            'コンタクトフォーム ページ プライバシーポリシー コメント欄 jp ' \
                            '２ちゃんねる運営 ヘルプ サイトポリシー ホームページ ' \
                            'リンク先 ビューワソフト一覧 利用規約 暗号化 JavaScript対応ブラウザ ' \
                            'グリル ノート 設定方法 上 他 上コメント投稿 ' \
                            'これから それから それなり から すぎ'.split(' ')
STOPWORDS_OF_WEBPAGE_VERB = 'メッセージ こちらの記事 クリックする 押す 入力する'.split(' ')
CLUES_FOR_OFFICIAL_PAGE = 'All Rights Reserved\tAll Right Reserved\tall rights reserved\tall right reverved\t' \
                          'copyright\tCopyright\t利用規約\tお問い合わせ\t' \
                          'お問いあわせ\tお問い合せ\tFAQ\tよくある質問'.split('\t')

CLUES_FOR_SHOPPING_PAGE = 'ショップ\tお買い上げ\t商品\tお支払い\tお客様\tお客さま\t特定商取引法に基づく表記'.split('\t')

ENTAILMENT_DICTIONARY_TYPES = 'entailing entailed'.split(' ')
SIMPLE_TASK_SEARCH_RESULTS_DIR_NAME = 'simple_task_search_results'
ACTION_WORD_IN_QUERY = 'を使う'
SO_CALLED = 'という'
QUERY = 'ビリヤード　プロ　なるには'

QUERIES_1 = '家庭菜園　始める,胃もたれ　防止する,ビリヤード　優勝する,花粉症　対策する,' \
            '保育園　入園させる,犬　育てる,部屋　掃除する,' \
            'クレー射撃　体験する'.split(',')

QUERIES_4 = '家庭菜園　を　始める,胃もたれ　を　防止する,ビリヤード　が　上手くなる,花粉症　を　対策する,' \
            '保育園　に　入園させる,犬　を　育てる,部屋　を　掃除する,' \
            'クレー射撃　を　体験する,野球　が　上手くなる,サッカー　が　上手くなる,ハンドボール　が　上手くなる'.split(',')

QUERIES_2 = 'カブトムシ　撮影する,ゴキブリ　対策する,' \
          '子供　なだめる,小学校　受験させる,大学　復学する,アメリカ　留学する,' \
          '禁煙　する,ストレス　解消する,夏バテ　防止する,頭痛　防止する,精神　鍛える,' \
          'アルバイト　見つける,生命保険　営業する,ページビュー　増やす,ブラック企業　辞める'.split(',')

QUERIES_3 = 'お金　儲ける,' \
          '暇　つぶす,ダイエット　する,英語　学習する,Ruby　学ぶ,発表　上達する,' \
          '自然言語処理　勉強する,' \
          'ダンス　上達する,草野球　試合する,プロテイン　購入する,ロードバイク　始める,ポーカー　稼ぐ,ドミニオン　遊ぶ,' \
          'ブルース・リーの映画　見る,中古ギター　入手する,ボーカル　録音する,ラノベ　デビューする,カメラ　上達する,同人ゲーム　宣伝する,' \
          '札幌　観光する,誕生日　祝う,結婚式　スピーチする,出産　祝う,ライブ　参加する,コミケ　準備する,学園祭　開催する,' \
          '荷物　送る,部屋　借りる,車　売却する,家具　捨てる,自転車　捨てる,ゴミ　捨てる,ブログ　炎上させる,' \
          '花見　満喫する,入学式　祝う,ゴールデンウィーク　遊ぶ,春　楽しむ,' \
          '街中　涼む,大文字　楽しむ,琵琶湖花火　満喫する,夏休み　過ごす,汗　対策する,' \
          '来客　もてなす'.split(',')  # 自然言語処理まで2014/01/27フェッチした
FINAL_QUERY = '家庭菜園　始める'
MIN_TFIDF = 0.1
TFIDF_RESULT_PKL_FILENAME = 'tfidf_result.pkl'
TFIDF_VECTORIZER_PKL_FILENAME = 'tfidf_vectorizer.pkl'

OBJECT_TERM_DICTIONARY_DIR_NAME = 'object_term_dictionary'
OBJECT_TERM_DICTIONARY_PICKLE_FILENAME = 'object_term_dictionary.pkl'

DIRECTIONS = ['ください','下さい', \
              'ましょう', \
              'なさい', \
              'しよう', \
              'べき', \
              'と良い','とよい', 'といい', \
              '必要があ', \
              'いかが', 'どうだろう']

PRONOUNS = 'それ あれ これ こちら そちら これら それら あれら'.split(' ')
DOTS = '. ! ? 。 ！ ？'.split(' ')
PICKLE_RESULT_DICT_NAME = 'hay_fever_result_dic.pkl'
NUM_OF_FETCHED_PAGES = 1000
NUM_OF_TOTAL_FETCHED_PAGES = 1000
NUM_OF_DEDUPLICATED_FETCHED_PAGES = 500

CLUE_WEB_URL_HEAD = 'http://karen.dl.local:8983/solr/ClueWeb09ja/select?q='
CLUE_WEB_URL_TAIL = '&wt=xml'

PARENTHESIS = '{ } [ ] < > 「 」 《 》 〈 〉 『 』 【 】 \' ’ \" ” "'.split(' ')
ROUND_PARENTHESIS = '( ) （ ）'.split(' ')
ALL_PARENTHESIS = PARENTHESIS + ROUND_PARENTHESIS

# を|に|へ|で|から
CMP_INFO_LIST = ['を\t助詞,格助詞,一般,*,*,*,を,ヲ,ヲ',
                 'へ\t助詞,格助詞,一般,*,*,*,へ,ヘ,エ',
                 'で\t助詞,格助詞,一般,*,*,*,で,デ,デ']

# からともはタスクではないとする
#                 'から\t助詞,格助詞,一般,*,*,*,から,カラ,カラ',
#                 'も\t助詞,係助詞,*,*,*,*,も,モ,モ']

# にだけは「選ぶようにしましょう」から「する」ではなく「選ぶ」となるよう気をつけねば
CMP_INFO_NI = 'に\t助詞,格助詞,一般,*,*,*,に,ニ,ニ'
CMP_INFO_YO = 'よう\t名詞,非自立,助動詞語幹,*,*,*,よう,ヨウ,ヨー'

TASK_WORDS = [
    'を使う', 'しましょう', 'てください', 'でください', 'で下さい', 'て下さい',
    'がおすすめ', 'がオススメ', '有効',
    'を選ぶ', 'してみては', 'するのがいい', 'するのがよい', 'するのが良い'
]
STOPWORDS = [
    '？', '?', '！', '!', '検索'
]

BLACK_WORDS = [
    'ログイン', 'サインイン', 'カート', '検索キーワード', '検索したい単語',
    'javascript', 'JavaScript', 'Javascript',
    'ボタンを押してください', '勝利馬券をゲット', '教えて', '助けて', '責任',
    'ご覧ください', 'JAPAN ID', '入力して', '無断転載', 'リンクを参照', '回答',
    'ノートに戻り、もう一度やり直してください', 'ページで登録されているノートを削除してください',
    'プレビューボタン', '注文手続きの際にお申し込み', 'Kindle化をご希望の場合',
    '</ul> <br /> <strong> 必ずお読みください', 'エラーが発生しました。やり直してください',
    '>もう一度試してください', '意見交換を通じて、お買い物にお役立てください',
    'Amazon.co.jp</a></b> が販売、発送します',
    'この機能は現在利用できません。しばらくしてからもう一度お試しください',
    '不適切な項目が含まれていることもあります。ご了承ください',
    'このユーザーのブロックを解除します', 'このユーザーをブロックします',
    '呼び出しを適切な位置に挿入してください',
    'このタグを +1 ボタンを表示する場所に挿入してください',
    '参考にしてみてください',
    'このトピックについて、他の呼び方、通称などがあれば登録してください',
    'メモやコメントの追加はここをクリックして下さい',
    'ノート</a>を参照してください',
    'この操作を実行するには、プライバシー設定を変更してください',
    '利用規約</a>を参照してください',
    'メニューを入れてください',
    'エリア、都道府県を選択してください',
    '観光地を選択してください',
    '+1 ボタン を表示したい位置に次のタグを貼り付けてください'
]
