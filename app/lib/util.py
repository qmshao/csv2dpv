import shutil
import os


def delete_folder(folder):
    shutil.rmtree(folder)
    os.mkdir(folder)