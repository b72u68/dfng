import os
import re
import sys
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
import processor

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/", methods=["POST"])
def home_search():
    q = request.form['q'] if 'q' in request.form else ''
    q = processor.preprocess_query(q)

    if not q:
        return redirect(url_for("home"))

    if 'k' not in request.form:
        return redirect(url_for("home"))

    try:
        k = int(request.form['k'].strip())
        return redirect(url_for("search_result", q=q, k=k))
    except Exception:
        return redirect(url_for("search_result", q=q, k=10))


@app.route("/search")
def search_result():
    q = request.args.get('q') if 'q' in request.args else ''
    q = processor.preprocess_query(q)

    if not q:
        return redirect(url_for("home"))

    if 'k' not in request.args:
        return redirect(url_for("search_result", q=q, k=10))

    try:
        k = int(request.args.get('k').strip())
    except Exception:
        k = 10

    result = processor.search(q, k)
    corrected_q = processor.spelling_correction(q)
    return render_template("result.html", q=q, k=k, result=result,
                           corrected_q=corrected_q)


@app.route("/search", methods=["POST"])
def search():
    q = request.args.get('q') if 'q' in request.args else ''
    q = processor.preprocess_query(q)

    if not q:
        return redirect(url_for("home"))

    if 'k' not in request.args:
        return redirect(url_for("search_result", q=q, k=10))

    if 'q' in request.form or not request.form['q'].strip():
        q = processor.preprocess_query(request.form['q'])

    try:
        init_k = int(request.args.get('k').strip())
        k = int(request.form['k']) if 'k' in request.form else init_k
    except Exception:
        k = 10

    return redirect(url_for("search_result", q=q, k=k))


if __name__ == "__main__":
    app.run(debug=True)
