import os
import shutil


class File(object):
    _data = {}

    def __init__(self, path):
        self.path = path
        self._load()

    def _load(self):
        temp = open(self.path, 'r')
        data = temp.readlines()
        self._data = {line.split('=')[0]: line.split('=')[1].replace('\n', '') for line in data}

    def _update(self):
        temp = open(self.path, 'w')
        for key in self._data:
            temp.write(key + '=' + str(self._data[key]) + '\n')
        temp.close()

    def set(self, *data):
        if len(data) == 1:
            if isinstance(data[0], dict):
                data = data[0]
                for i in data:
                    self._data[i] = data[i]
        elif len(data) == 2:
            self._data[data[0]] = data[1]
        self._update()

    def remove(self, key):
        if key in self._data:
            del self._data[key]
            self._update()

    def rename(self, new_path):
        if os.path.isfile(new_path):
            raise OSError("File already exists.")
        else:
            os.rename(self.path, new_path)
            self.path = new_path

    def delete(self):
        os.remove(self.path)

    def read(self, key):
        return self._data[key]


class Directory(object):

    def __init__(self, path):
        self.path = path

    def rename(self, new_path):
        if os.path.isdir(new_path):
            raise OSError("Directory already exists.")
        else:
            os.rename(self.path, new_path)
            self.path = new_path

    def remove(self):
        shutil.rmtree(self.path)


class Utilities(object):
    @staticmethod
    def create_file(path):
        if os.path.isfile(path):
            raise OSError("File already exists.")
        else:
            f = open(path, 'a')
            f.close()
            return File(path)

    @staticmethod
    def open_file(path):
        if os.path.exists(path):
            return File(path)
        else:
            raise OSError("File doesn\'t exist")

    @staticmethod
    def create_dir(path):
        if os.path.exists(path):
            raise OSError("Directory already exists.")
        else:
            os.makedirs(path)

    @staticmethod
    def open_dir(path):
        if os.path.isdir(path):
            return Directory(path)
        else:
            raise OSError("Directory doesn\'t exist")

    @staticmethod
    def path_exists(path):
        return os.path.exists(path)
