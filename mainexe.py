import multiprocessing

from main import run
from src.shared.utils.resources import resource_path

if __name__ == "__main__":
    multiprocessing.freeze_support()
    run(str(resource_path("execonfig.json")))
