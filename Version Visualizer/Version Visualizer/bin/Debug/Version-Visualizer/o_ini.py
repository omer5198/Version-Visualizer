import os
import shutil

class File(object):
    def __init__(self, path):
        self.path = path

    def rename(self, new_name):
        new_path = Utilities.getParentPath(self.path) + '\\' + new_name
        if os.path.isfile(new_path):
            raise OSError("File already exists.")
        else:
            os.rename(self.path, new_path)
            self.path = new_path

    def delete(self):
        os.remove(self.path)



class oFile(File):
    _data = {}
    def __init__(self, path):
        File.__init__(self, path)
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
    def read(self, key):
        return self._data[key]

    def readall(self):
        return self._data.values()

    def readkeys(self):
        return self._data.keys()


class Directory(object):

    def __init__(self, path):
        self.path = path

    def rename(self, new_name):
        new_path = Utilities.getParentPath(self.path) + '\\' + new_name
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
    def create_o_file(path):
        if os.path.isfile(path):
            raise OSError("File already exists.")
        else:
            f = open(path, 'a')
            f.close()
            return oFile(path)
    @staticmethod
    def open_o_file(path):
        if os.path.exists(path):
            return oFile(path)
        else:
            raise OSError("File doesn\'t exist")
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
            return Directory(path)

    @staticmethod
    def open_dir(path):
        if os.path.isdir(path):
            return Directory(path)
        else:
            raise OSError("Directory doesn\'t exist")

    @staticmethod
    def path_exists(path):
        return os.path.exists(path)
    @staticmethod
    def getParentPath(path):
        return os.path.abspath(os.path.join(path, os.pardir))
    @staticmethod
    def getBaseName(path):
        return os.path.basename(path)
