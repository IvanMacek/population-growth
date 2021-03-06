import os
from dataclasses import asdict

from flask import Flask, jsonify

from model import SearchEngine

app = Flask(__name__)

search_engine = SearchEngine(zip_to_cbsa_url=os.environ['ZIP_TO_CBSA_URL'], cbsa_to_msa_url=os.environ['CBSA_TO_MSA_URL'])


@app.route("/search-zip/<zip_parameter>")
def search_by_zip(zip_parameter):
    try:
        zip_code = int(zip_parameter)
    except ValueError:
        return jsonify(error='Invalid zip code'), 404

    search_result = search_engine.search_by_zip(zip_code)
    return jsonify(asdict(search_result))


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)))
