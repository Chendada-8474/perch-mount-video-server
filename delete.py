from src import utils
import logging

logging.basicConfig(filename="delete.log", filemode="w", level=logging.DEBUG)


if __name__ == "__main__":
    num_detected = utils.detect_run()
    print(num_detected, "done")
