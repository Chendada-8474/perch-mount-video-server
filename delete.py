from src import utils
import logging

logging.basicConfig(
    filename="delete.log", encoding="utf-8", filemode="w", level=logging.DEBUG
)


if __name__ == "__main__":
    num_detected = utils.delete_run()
    print(num_detected, "done")
