from Project import *
from o_ini import *
import os
Utilities.create_file('test.py')
raw_input('test file created.')
p = create_project(os.path.dirname(os.path.abspath(__file__)), 'Test')
raw_input('project created.')
p.add_file('test.py')
raw_input('file added to project.')
p.save_file_version('test.py')
raw_input('saved version')
p.save_file_version('test.py', 'WithComment')
raw_input('saved another version')
versions = p.get_history_list('test.py')
print 'versions: ', versions
print 'LAST VERSION:'
data = p.get_file_version('test.py', versions[-1])
with open('test2.py', 'wb') as f:
    f.write(data)