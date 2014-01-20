# -*- coding: utf-8 -*-
FETCHED_PAGES_DIR_NAME = 'fetched_pages'
FETCHED_ADS_DIR_NAME = 'fetched_ads'
QUERIES_DIR_NAME = 'queries'
ENTAILMENT_DICTIONARIES_DIR_NAME = 'entailment_dictionaries'
ENTAILMENT_DICTIONARY_NAMES = 'ent_presu ent_triv nonent_predi ent_ntriv nonent_ntriv'.split(' ')
ENTAILMENT_DICTIONARY_TABLENAMES = 'entailment_acrac entailment_ntriv entailment_presu entailment_triv nonentailment_anton nonentailment_ntriv nonentailment_predi nonentailment_triv'.split(' ')
ENTAILMENT_DICTIONARY_TYPES = 'entailing entailed'.split(' ')
SIMPLE_TASK_SEARCH_RESULTS_DIR_NAME = 'simpla_task_search_results'
ACTION_WORD_IN_QUERY = 'を使う'
SO_CALLED = 'という'
QUERY = 'ビリヤード　プロ　なるには'
QUERIES = '花粉症　対策する,部屋　掃除する,クレー射撃　体験する,' \
          '家庭菜園　始める,犬　育てる,胃もたれ　防止する,' \
          '保育園　入園させる,骨折　治療する,ビリヤード　優勝する,ノベルゲーム　完成させる'.split(',')
# FINAL_QUERY = QUERY + '　"' + ACTION_WORD_IN_QUERY + '"'
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
NUM_OF_FETCHED_PAGES = 50
NUM_OF_TOTAL_FETCHED_PAGES = 94
CLUE_WEB_URL_HEAD = 'http://karen.dl.local:8983/solr/ClueWeb09ja/select?q='
CLUE_WEB_URL_TAIL = '&wt=xml'

PARENTHESIS = '{ } [ ] < > 「 」 《 》 〈 〉 『 』 【 】 \' ’ \" ” "'.split(' ')
ROUND_PARENTHESIS = '( ) （ ）'.split(' ')
ALL_PARENTHESIS = PARENTHESIS + ROUND_PARENTHESIS

# を|に|へ|で|から
CMP_INFO_LIST = ['を\t助詞,格助詞,一般,*,*,*,を,ヲ,ヲ',
                 'へ\t助詞,格助詞,一般,*,*,*,へ,ヘ,エ',
                 'で\t助詞,格助詞,一般,*,*,*,で,デ,デ',
                 'から\t助詞,格助詞,一般,*,*,*,から,カラ,カラ']

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
