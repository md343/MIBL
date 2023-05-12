import os


def check_dir(save_directory):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    return save_directory

def clean_dir(dir):
    for file in os.listdir(dir):
        file_path = dir.joinpath(file)
        os.remove(file_path)
