import shutil
import os
failed = 0
while failed < 3:
    failed = 0
    try:
        shutil.rmtree('Test')
        os.remove('Test')
    except:
        failed += 1
        print 'failed'
    try:
        os.remove('bla.py')
    except:
        failed += 1
        print 'failed'
    try:
        os.remove('test.py')
    except:
        failed += 1
        print 'failed'