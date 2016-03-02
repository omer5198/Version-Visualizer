import diff_match_patch
from base64 import b64encode, b64decode
name1 = 'old.txt'
name2 = 'new.txt'

f = open(name1, 'r').read()
g = open(name2, 'r').read()
h = open('diffs.txt', 'w')

dmp = diff_match_patch.diff_match_patch()
patch = dmp.patch_make(b64encode(f), b64encode(g))
h.write(dmp.patch_toText(patch))
h.close()
