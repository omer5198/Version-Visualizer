import os
from o_ini import *
from time import strftime
import shutil
import diff_match_patch

class Project(object):

    def __init__(self, name, config):
        self.name = name
        self.config = config

    def get_name(self):
        return self.name

    def get_files_names(self):
        temp = Utilities.open_o_file(self.config)
        return temp.readkeys()

    def get_files_paths(self):
        temp = Utilities.open_o_file(self.config)
        return temp.readall()

    def get_file_path(self, file_name):
        f = Utilities.open_o_file(self.config)
        return f.read(file_name)

    def get_basefile_path(self, file_name):
        return Utilities.getParentPath(self.config) + '\\' + file_name + '\\basefile' + \
               os.path.splitext(file_name)[1]

    def renameProject(self, new_name):
        dir = Utilities.open_dir(Utilities.getParentPath(self.config))
        dir.rename(new_name)

    def delete_project(self):
        dir = Utilities.open_dir(Utilities.getParentPath(self.config))
        dir.remove()

    def add_file(self, path):
        if not Utilities.path_exists(path):
            raise OSError('File doesn\'t exist.')
        f = Utilities.open_o_file(self.config)
        file_name = Utilities.getBaseName(path)
        f.set(file_name, path)
        Utilities.create_dir(Utilities.getParentPath(self.config) + '\\' + file_name)
        Utilities.create_dir(Utilities.getParentPath(self.config) + '\\' + file_name + '\\Versions')
        shutil.copyfile(self.get_file_path(file_name), Utilities.getParentPath(self.config) + '\\' + file_name +
                        '\\basefile' + os.path.splitext(file_name)[1])

    def remove_file(self, file_name):
        f = Utilities.open_o_file(self.config)
        self.save_file_version(file_name, 'DELETED')
        temp = Utilities.open_dir(Utilities.getParentPath(self.config) + '\\' + file_name)
        temp.rename(file_name + ' [DELETED]')
        #temp = Utilities.open_file(self.get_file_path(file_name))
        #temp.delete()
        f.remove(file_name)


    def rename_file(self, file_name, new_name):
        f = Utilities.open_o_file(self.config)
        f.set(new_name, Utilities.getParentPath(self.get_file_path(file_name)) + '\\' + new_name)
        temp = Utilities.open_file(self.get_file_path(file_name))
        temp.rename(new_name)
        temp = Utilities.open_dir(Utilities.getParentPath(self.config) + '\\' + file_name)
        temp.rename(new_name)
        f.remove(file_name)
        # Rename VersionHistry (?)

    def get_file(self, path):
        return File(path)

    def get_history_list(self, file_name):
        return os.listdir(Utilities.getParentPath(self.config) + '\\' + file_name + '\\Versions')

    def save_file_version(self, file_name, comment = ''):
        versions = self.get_history_list(file_name)
        with open(self.get_file_path(file_name), 'r') as f, \
                open(Utilities.getParentPath(self.config) + '\\' + file_name + '\\Versions\\' + strftime('%d-%m-%y--%H-%M-%S.txt'), 'w') as h:
            dmp = diff_match_patch.diff_match_patch()
            if versions:
                patch = dmp.patch_make(self.get_file_version(file_name, versions[-1]), f.read())
            else:
                patch = dmp.patch_make(self.get_file_version(file_name, []), f.read())
            h.write(dmp.patch_toText(patch))

    def get_file_version(self, file_name, version):
        if not version:
            with open(self.get_basefile_path(file_name), 'r') as f:
                return f.read()
        versions = self.get_history_list(file_name)
        shutil.copyfile(Utilities.getParentPath(self.config) + '\\' + file_name + '\\basefile' + os.path.splitext(file_name)[1],
                        Utilities.getParentPath(self.config) + '\\' + file_name + '\\temp.txt')
        for i in xrange(versions.index(version) + 1):
            with open(Utilities.getParentPath(self.config) + '\\' + file_name + '\\Versions\\' + versions[i]) as g, \
                    open(Utilities.getParentPath(self.config) + '\\' + file_name + '\\temp.txt', 'r+') as temp:
                dmp = diff_match_patch.diff_match_patch()
                patch_text = g.read()
                print '******** P A T C H - T E X T **********'
                print patch_text
                patch = dmp.patch_fromText(patch_text)
                patched = dmp.patch_apply(patch, temp.read())[0]
                print "******* P A T C H E D - D A T A *********"
                print patched
                temp.seek(0)
                temp.truncate()
                temp.write(patched)
        with open(Utilities.getParentPath(self.config) + '\\' + file_name + '\\temp.txt', 'r') as temp:
            data = temp.read()
        os.remove(Utilities.getParentPath(self.config) + '\\' + file_name + '\\temp.txt')
        return data


def create_project(path, name, files_paths=[]):
    Utilities.create_dir(path + '\\' + name)
    Utilities.create_o_file(path + '\\' + name + '\\config.ini')
    p = Project(name, path + '\\' + name + '\\config.ini')
    for file in files_paths:
        p.add_file(file)
    return p

def open_project(path, name):
    if not Utilities.path_exists(path + '\\' + name + '\\config.ini'):
        raise OSError('Project doesn\'t exist.')
    p = Project(name, path + '\\' + name + '\\config.ini')
    return p
