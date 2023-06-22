import os


def ensure_path_exists(path):
    dir_name = os.path.dirname(path)

    # Create the directory if it does not exist
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # Create the file if it does not exist
    if not os.path.isfile(path):
        open(path, 'w').close()
