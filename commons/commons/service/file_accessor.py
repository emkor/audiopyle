import os


class FileAccessor(object):
    @staticmethod
    def exists(file_path):
        return FileAccessor.is_dir(file_path) or FileAccessor.is_file(file_path)

    @staticmethod
    def is_file(file_path):
        return os.path.isfile(os.path.normpath(file_path))

    @staticmethod
    def is_dir(file_path):
        return os.path.isdir(os.path.normpath(file_path))

    @staticmethod
    def get_file_name(file_path):
        return os.path.basename(os.path.normpath(file_path))

    @staticmethod
    def join(*path_parts):
        normed = [os.path.normpath(path) for path in path_parts]
        return os.path.join(normed[0], *(normed[1:]))

    @staticmethod
    def remove_file(file_path):
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            print(e)
            return False