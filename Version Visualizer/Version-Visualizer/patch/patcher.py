import diff_match_patch
from base64 import b64encode, b64decode
name1 = 'old.txt'
name2 = 'diffs.txt'

f = open(name1, 'r').read()
g = open(name2, 'r').read()
h = open('patched.txt', 'w')
dmp = diff_match_patch.diff_match_patch()
patch = dmp.patch_fromText(g)
h.write(b64decode(dmp.patch_apply(patch, b64encode(f))[0]))
h.close()
