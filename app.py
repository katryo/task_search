from flask import Flask, render_template, request
import constants
from search_engine import SearchEngine
from web_page import WebPage
import pdb
app = Flask(__name__)
app.config.from_object(constants)

@app.route("/")
def index(name=None):
    return render_template("base.html", name=name)

@app.route("/search", methods=["post"])
def search():
    pages = search_by_google_or_bing(request)
    return render_template("results.tmpl", items=pages)

@app.route("/search_and_fetch_headers", methods=["post"])
def search_and_fetch_headers():
    pages = search_by_google_or_bing(request)
    trees = []
    for page in pages:
        html = page.fetch_html()
        page.build_header_tree()
        tree = page.header_tree()
        trees.append(tree)
    return render_template("results.tmpl", trees=trees)

def search_by_google_or_bing(request):
    query = request.form["query"]
    search_engine_name = request.form['search_engine']
    search_engine = SearchEngine()
    if search_engine_name == 'google':
        pages = search_engine.google_search(query, 1)
    else:
        pages = search_engine.bing_search(query, 1)
    return pages


@app.route('/find_related_action_words', methods=['post'])
def find_related_action_words():
    search_engine = SearchEngine()
    search_engine.action_word = request.form['action_word']
    search_engine.hint_word = request.form['hint_word']
    search_engine.find_related_action_words()
    search_engine.count_action_words()
    search_engine.sort_action_words_count()
    for elem in search_engine.sorted_action_words:
        elem['expanded_query'] = search_engine.action_word + ' ' + search_engine.hint_word + ' ' + elem['word']
    return render_template('find_related_action_words.tmpl', items=search_engine.result_pages, sorted_action_words=search_engine.sorted_action_words, found_pages=search_engine.material_pages, query=search_engine.actual_query)

@app.route('/search_in_clueweb_with_expanded_query', methods=['post'])
def search_in_clueweb_with_expanded_query():
    search_engine = SearchEngine()
    search_engine.action_word = request.form['action_word']
    search_engine.hint_word = request.form['hint_word']
    search_engine.find_related_action_words_with_google()
    search_engine.count_action_words()
    search_engine.sort_action_words_count()
    search_engine.pick_sorted_action_words_more_than_1_count()
    results = []
    for elem in search_engine.sorted_action_words_more_than_1_count:
        elem['expanded_query'] = search_engine.action_word + ' ' + search_engine.hint_word + ' ' + elem['word']
        url = 'http://karen.dl.local:8983/solr/ClueWeb09ja/select?q=' + elem['expanded_query'] + '&wt=xml'
        web_page = WebPage(url)
        web_page.fetch_xml()
        web_page.pick_texts_to_result_pages()
        # クエリ1つごとに結果xmlページがある
        # 結果xmlページの内容を1ページずつWebPageオブジェクトにしてresult_pagesとして1クエリに対応する結果ページに持たせる
        for result_page in web_page.result_pages:
            # result_page.text_body
            result_page.set_lines_from_texts()
            result_page.set_line_nums_with_word(search_engine.action_word)
            result_page.set_line_nums_around_action_word()
            result_page.set_line_clusters_around_action_word()
        # web_page.result_pages[0].line_clusters_around_action_word
        results.append({'pages': web_page.result_pages, 'expanded_query': elem['expanded_query']})
    return render_template('search_in_clueweb_with_expanded_query.tmpl',
        results=results)

@app.route('/find_words_with_yahoo_ads', methods=['post'])
def yahoo_sponsored_results():
    query = request.form['query']
    #yahooスポンサードサーチは単語ごとに区切るより一文にしたほうが広告出やすい
    head = 'http://search.yahoo.co.jp/search/ss?p='
    tail = '&ei=UTF-8&fr=top_ga1_sa&type=websearch&x=drt'
    url = head + query + tail
    y_ad_page = WebPage(url)
    y_ad_page.fetch_html()
    y_ad_page.fetch_ads()
    result_words = []
    key_phrases_of_ads = []
    Engine = SearchEngine()
    for ad in y_ad_page.ads:
        result_words.extend(ad.pick_nouns_and_verbs(ad.title))
        result_words.extend(ad.pick_nouns_and_verbs(ad.snippet))
        #key_phrases_of_ads.append(Engine.yahoo_key_phrase(ad.title))
        #key_phrases_of_ads.append(Engine.yahoo_key_phrase(ad.snippet))
    results = to_ranked_items(result_words)
    #return ad_template.render(items=results)
    return render_template('find_words_with_yahoo_ads.tmpl',
        items=results)

@app.route('/find_matched_words_from_yahoo_ads', methods=['post'])
def find_matched_words_from_yahoo_ads():
    query = request.form['query']
    #yahooスポンサードサーチは単語ごとに区切るより一文にしたほうが広告出やすい
    head = 'http://search.yahoo.co.jp/search/ss?p='
    tail = '&ei=UTF-8&fr=top_ga1_sa&type=websearch&x=drt'
    url = head + query + tail
    y_ad_page = WebPage(url)
    y_ad_page.fetch_html()
    y_ad_page.fetch_ads()
    naradeha_results = []
    bracket_words = []
    for ad in y_ad_page.ads:
        ad.fetch_link_title()
        naradeha_results.extend(ad.pick_characteristic_words())
        bracket_words.extend(ad.pick_bracket_words())
    # naradeharesults => [{'なら': {'before': ['。', 'あの', '今石洋之']}}]
    # bracket_words => ['アスコルビン酸', 'メルトダウン']

    stop_words = ['公式', '楽天', '当日', 'お急ぎ便', 'ココ', 'ここ', 'これ', 'コレ', 'こちら', '公式', '購入', '人気', '詳細', '送料無料', '配送無料', '価格', '激安', '無料', 'アマゾン', 'ヤフオク', '０', '１', '２', '３']
    for num in range(0, 10):
        stop_words.append(str(num))
    results = naradeha_words_to_results(naradeha_results, stop_words)

    for bracket_word in bracket_words:
        is_including_stop_word = False
        for stop_word in stop_words:
            if stop_word in bracket_word:
                is_including_stop_word = True
                break
        if is_including_stop_word:
            continue
        results.append(bracket_word)

    return render_template('words.tmpl', words=results)


@app.route('/scrape_from_nanapi', methods=['post'])
def scrape_from_nanapi():
    query = request.form['query']
    #yahooスポンサードサーチは単語ごとに区切るより一文にしたほうが広告出やすい
    head = 'http://nanapi.jp/search/q:'
    query_url = head + query
    nanapi_search_result_page = WebPage(query_url)
    nanapi_search_result_page.fetch_html()
    urls = nanapi_search_result_page.find_urls_from_nanapi_search_result()
    tasks = []
    for url in urls:
        # result_pageはnanapiの1記事
        result_page = WebPage(url)
        result_page.fetch_html()
        # task_steps => [task_step, task_step, ...]
        task = result_page.find_task_from_nanapi_with_headings()
        # task_steps[0].h2 => 'はじめに'
        # task_steps[0].h3s[0] => 'はじめに'
        tasks.append(task)
    # tasks => [task, task, ...]
    # tasks[0][0].h2 => 'はじめに'
    return render_template('nanapi_tasks.tmpl', tasks=tasks)


#https://www.google.com/search?as_q=flamenco&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr=&as_qdr=all&as_sitesearch=www.wikihow.com&as_occt=any&safe=images&as_filetype=&as_rights=


def naradeha_words_to_results(naradeha_results, stop_words):
    results = []
    for result in naradeha_results:
        for nara_de_ha in ['nara', 'de', 'ha']:
            for key in ['before', 'after']:
                if not result[nara_de_ha][key]:
                    continue
                answer = ''.join(result[nara_de_ha][key])
                # beforeやafterが空白のとき
                is_including_stop_word = False
                for stop_word in stop_words:
                    if stop_word in answer:
                        is_including_stop_word = True
                        break
                if is_including_stop_word:
                    continue
                results.append(answer)
    return results

def to_ranked_items(items):
    rank_dict = {}
    #items => ['対策', '鼻炎', '対策', 'うるおい', ...]
    for item in items:
        if item in rank_dict.keys():
            rank_dict[item] += 1
        else:
            rank_dict[item] = 1
    #rank_dict => {'対策': 2, '鼻炎': 1, ...}
    keys = rank_dict.keys()  # => ['対策', '鼻炎', ...]
    results = []
    for key in keys:
        count = rank_dict[key]  # => 2
        result = {'name': key, 'count': count}
        results.append(result)
    #results => [{'name': '対策', 'count': 2},  ....]
    outputs = divide_by_count(results)
    return outputs


def divide_by_count(items):
    high_items = []
    middle_items = []
    low_items = []
    for item in items:
        if item['count'] > 2:
            high_items.append(item)
        elif item['count'] == 2:
            middle_items.append(item)
        else:
            low_items.append(item)
    outputs = []
    outputs.extend(high_items)
    outputs.extend(middle_items)
    outputs.extend(low_items)
    return outputs



if __name__ == "__main__":
    app.run(debug=True)
