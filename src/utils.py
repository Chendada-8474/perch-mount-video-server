import datetime
import os
import uuid
import tqdm
import json
import shutil
import pathlib
import logging
from minio import Minio
from src import config


DETECTE_RUN_DURATION = 2
TODAY = datetime.datetime.now().strftime("YYYY-MM-DD")


class Hierarchy:
    project = None
    perch_mount_name = None
    check_date = None

    def __init__(self, path: str) -> None:
        self._get_hierarchy(path)

    def _get_hierarchy(self, path: str) -> dict:
        hierarchy = str(pathlib.Path(path)).split("\\")
        self.project = hierarchy[-4]
        self.perch_mount_name = hierarchy[-3]
        self.check_date = hierarchy[-2]
        self.file_name = hierarchy[-1]


client = Minio(
    config.MINIO_HOST,
    access_key=config.MINIO_ACCESS_KEY,
    secret_key=config.MINIO_SECRET_KEY,
    secure=False,
)


def save_data_as_json(data):
    file_name = str(uuid.uuid4()) + ".json"
    with open(os.path.join(config.TASKS_DIR, file_name), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def make_empty_dir():
    dir_path = os.path.join(config.EMPTY_MEDIA_DIR, TODAY)
    pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)


def read_task(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def _get_hierarchy(path: str) -> Hierarchy:
    return Hierarchy(path)


def _detect_media(media: list[dict]):

    objects = []

    for medium in tqdm.tqdm(media):
        hierarchy = _get_hierarchy(medium["path"])

        objects.append(
            os.path.join(
                hierarchy.project,
                hierarchy.perch_mount_name,
                hierarchy.check_date,
                medium["medium_id"] + ".JPEG",
            )
        )

        try:
            shutil.move(
                medium["path"],
                os.path.join(config.EMPTY_MEDIA_DIR, TODAY, hierarchy.file_name),
            )
        except Exception as e:
            logging.error(e)
    try:
        client.remove_objects(config.MINIO_BUCKET, objects)
    except Exception as e:
        logging.error(e)


def delete_run():
    make_empty_dir()
    tasks = os.listdir(config.TASKS_DIR)

    print(f"pending {len(tasks)} jobs")

    stop_at = datetime.datetime.now() + datetime.timedelta(hours=DETECTE_RUN_DURATION)
    count = 0
    for file_name in tasks:
        task_path = os.path.join(config.TASKS_DIR, file_name)
        task = read_task(task_path)
        _detect_media(task)
        count += 1
        shutil.move(task_path, os.path.join(config.DONE_TASKS_DIR, file_name))
        if datetime.datetime.now() > stop_at:
            break
    return count
