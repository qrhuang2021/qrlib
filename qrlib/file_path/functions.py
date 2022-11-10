import os


def have_corresponding_file(path, corresponding_file_extention):
    assert corresponding_file_extention[0] == '.'
    _, filename = os.path.split(path)
    _, extention = os.path.splitext(filename)
    return os.path.exists(path.replace(extention, corresponding_file_extention))


def change_ext(path, target_ext):
    # assert os.path.isfile(path)
    assert target_ext.startswith('.')
    _, ext = os.path.splitext(path)
    return path.replace(ext, target_ext)


def add_prefix(path, prefix):
    # assert os.path.isfile(path)
    dir_, filename = os.path.split(path)
    new_filename = '{}{}'.format(prefix, filename)
    return os.path.join(dir_, new_filename)


def analyse_path(path):
    dir_, filename_with_ext = os.path.split(path)
    filename_wo_ext, extention = os.path.splitext(filename_with_ext)
    return dir_, filename_wo_ext, extention