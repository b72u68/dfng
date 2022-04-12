import json
from flask import Flask
from flask import request
from processor import Processor

app = Flask(__name__)
processor = Processor()


@app.route("/search")
def search():
    content = request.json
    q = content.get('q') if 'q' in content else ''
    k = content.get('k') if 'k' in content else 10

    q = processor.preprocess_query(q)

    if not q:
        data = {"message": "invalid search query"}
        return json.dumps(data)

    if isinstance(k, str) and not k.isnumeric():
        data = {"message": "invalid top-K value"}
        return json.dumps(data)

    corrected_query = processor.spelling_correction(q)

    result = processor.search(q, int(k))
    data = {"q": q, "corrected_q": corrected_query, "k": int(k),
            "total": len(result), "result": result}

    return json.dumps(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
