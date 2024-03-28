import base64
import flask

from src import utils

app = flask.Flask(__name__)


@app.route("/video/<string:base32_path>", methods=["GET"])
def video(base32_path: str):
    try:
        path = base32_path.encode("utf-8")
        path = base64.b32decode(path)
        path = path.decode("utf-8")
        return flask.send_file(path)
    except:
        return flask.jsonify({"message": "video not found"}, 404)


@app.route("/delete_media", methods=["POST"])
def post_task():
    task = flask.request.get_json()
    utils.save_data_as_json(task)
    return flask.jsonify({"message": "task saved"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
