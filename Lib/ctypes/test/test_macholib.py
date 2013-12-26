import os
import sys
import unittest

# Bob Ippolito:
#
# Ok.. the code to find the filename for __getattr__ should look
# something like:
#
# import os
# from macholib.dyld import dyld_find
#
# def find_lib(name):
#      possible = ['lib'+name+'.dylib', name+'.dylib',
#      name+'.framework/'+name]
#      for dylib in possible:
#          try:
#              return os.path.realpath(dyld_find(dylib))
#          except ValueError:
#              pass
#      raise ValueError, "%s not found" % (name,)
#
# It'll have output like this:
#
#  >>> find_lib('pthread')
# '/usr/lib/libSystem.B.dylib'
#  >>> find_lib('z')
# '/usr/lib/libz.1.dylib'
#  >>> find_lib('IOKit')
# '/System/Library/Frameworks/IOKit.framework/Versions/A/IOKit'
#
# -bob

from ctypes.macholib.dyld import dyld_find

def find_lib(name):
    possible = ['lib'+name+'.dylib', name+'.dylib', name+'.framework/'+name]
    for dylib in possible:
        try:
            return os.path.realpath(dyld_find(dylib))
        except ValueError:
            pass
    raise ValueError("%s not found" % (name,))

class MachOTest(unittest.TestCase):
    if sys.platform == "darwin":
        def test_find(self):

            self.assertEqual(find_lib('pthread'),
                                 '/usr/lib/libSystem.B.dylib')

            result = find_lib('z')
            self.assertTrue(result.startswith('/usr/lib/libz.1'))
            self.assertTrue(result.endswith('.dylib'))

            self.assertEqual(find_lib('IOKit'),
                                 '/System/Library/Frameworks/IOKit.framework/Versions/A/IOKit')

if __name__ == "__main__":
    unittest.main()
