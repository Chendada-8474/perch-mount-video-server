import datetime
import os
import uuid
import json


DETECTE_RUN_DURATION = 2


def save_data_as_json(data):
    file_name = str(uuid.uuid4()) + ".json"
    with open(f"./tasks/{file_name}", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def _detect_media(paths: list[str]):
    for path in paths:
        os.remove(path)


def detect_run():
    tasks = os.listdir("./tasks")
    stop_at = datetime.datetime.now() + datetime.timedelta(hours=DETECTE_RUN_DURATION)
    count = 0
    for task in tasks:
        _detect_media(task)
        count += 1
        if datetime.datetime.now() > stop_at:
            return
    return count
