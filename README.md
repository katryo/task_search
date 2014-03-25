task_search
===========

## 目的
Bing APIを使ってWeb検索を行い、クエリに応じたタスクの目的を達成する方法を見つけるシステムです

## 使い方
1. my_keysのmy_keys.MICROSOFT_API_KEYにBing APIのキーを書く
2. costants.QUERIES_4にクエリをlist形式で書く
3. fetch_web_pages_with_original_queries.pyを実行。BingAPIで取得したWebPageオブジェクトをPickle化して保存する。
4. fetch_and_set_sentences_to_pages_with_original_queries.pyを実行。WebPageオブジェクトにhtmlをセットする。
5. set_tasks_to_fetched_pages_for_original.pyを実行。WebPageオブジェクトにTasksオブジェクトをAttributeとしてセットする。
