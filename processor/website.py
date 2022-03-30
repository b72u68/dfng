import os
import re
import sys
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from indexer.indexer import Indexer

app = Flask(__name__)
indexer = Indexer()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/", methods=["POST"])
def home_search():
    q = request.form['q'].strip() if 'q' in request.form else ''
    q = preprocess_query(q)
    k = int(request.form['k'].strip()) if 'k' in request.form else 10
    return redirect(url_for("search_result", q=q, k=k))


@app.route("/search")
def search_result():
    if 'q' not in request.args:
        return redirect(url_for("home"))

    q = request.args.get('q')
    if 'k' not in request.args:
        return redirect(url_for("search_result", q=q, k=10))

    try:
        k = int(request.args.get('k').strip())
        result = search_index(q, k)
        return render_template("result.html", q=q, k=k, result=result)
    except Exception:
        result = search_index(q, 10)
        return render_template("result.html", q=q, k=10, result=result)


@app.route("/search", methods=["POST"])
def search():
    if 'q' not in request.args or not request.args.get('q').strip():
        return redirect(url_for("home"))
    q = preprocess_query(request.args.get('q'))
    if 'k' not in request.args:
        return redirect(url_for("search_result", q=q, k=10))
    init_k = int(request.args.get('k').strip())
    k = int(request.form['k']) if 'k' in request.form else init_k
    if 'q' in request.form:
        q = request.form['q']
    return redirect(url_for("search_result", q=q, k=k))


def preprocess_query(query):
    query = re.sub(r'[\t\n\r]', ' ', query)
    query = re.sub(r'\s+', ' ', query).strip()
    return query


def search_index(query, top_k=10):
    index = indexer.load_index()
    query = indexer.tokenize(query)
    return indexer.search(index, query, top_k)


if __name__ == "__main__":
    app.run(debug=True)
