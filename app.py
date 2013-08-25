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
    query = request.form["query"]
    search_engine = SearchEngine()
    pages = search_engine.google_search(query, 5)
    return render_template("results.tmpl", items=pages)

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
    search_engine.find_related_action_words()
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



if __name__ == "__main__":
    app.run(debug=True)
