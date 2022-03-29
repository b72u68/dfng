from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/", methods=["POST"])
def home_search():
    q = request.form['q'].strip() if 'q' in request.form else ''
    k = int(request.form['k'].strip()) if 'k' in request.form else 10
    return redirect(url_for("search", q=q, k=k))


@app.route("/search")
def search_result():
    if 'q' not in request.args:
        return redirect(url_for("home"))
    q = request.args.get('q').strip()
    if 'k' not in request.args:
        return redirect(url_for("search", q=q, k=10))
    k = int(request.args.get('k').strip())
    return render_template("result.html", q=q, k=k)


@app.route("/search", methods=["POST"])
def search():
    if 'q' not in request.args:
        return redirect(url_for("home"))
    q = request.args.get('q').strip()
    if 'k' not in request.args:
        return redirect(url_for("search", q=q, k=10))
    init_k = int(request.args.get('k').strip())
    k = int(request.form['k']) if 'k' in request.form else init_k
    if 'q' in request.form and request.form['q'].strip():
        q = request.form['q'].strip()
    return redirect(url_for("search", q=q, k=k))


if __name__ == "__main__":
    app.run(debug=True)
