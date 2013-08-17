from flask import Flask, render_template, request
import constants
from search_engine import SearchEngine
import pdb
app = Flask(__name__)
app.config.from_object(constants)

@app.route("/")
def index(name=None):
    return render_template("base.html", name=name, a=app.config["AA"])

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
    return render_template('find_related_action_words.tmpl', items=search_engine.result_pages, sorted_action_words=search_engine.sorted_action_words, found_pages=search_engine.material_pages, query=search_engine.actual_query)

if __name__ == "__main__":
    app.run(debug=True)
