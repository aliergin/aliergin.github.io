
#
# PxM 
# Detects:
#   PPM (P6)
# TODO: all others format :)
#

import re

def identify_P6(h):

  if h[0] == '#':
    raise "I don't support comment in a PPM file"

  m = re.search("^(\d+)\s(\d+)", h)
  if not m:
    return (None, None)
  # The third line can be skipped
  return ('PPM',((int(m.group(1)), int(m.group(2)))))


def identify(filename):

  h = None
  f = open(filename,'rb')
  if not f:
    return (None, None)
  h = f.read(1024)
  f.close()

  # PPM has an ASCII header on the first line
  if h[0:3] == 'P6\n':
    return identify_P6(h[3:])
  return (None, None)

if __name__ == "__main__":
#   import profile
#   profile.run('main()')
    import sys
    import PxM
    
    if len(sys.argv) < 2:
      print 'Usage: %s files...\n' % sys.argv[0]
      sys.exit(0)
        
    for filename in sys.argv[1:]:
        (format, info)=PxM.identify(filename)
	if info != None:
	  print "%s (format=%s; size = %d,%d)" % (filename,format, info[0],info[1])
	else:
	  print "%s is not a PPM,PGM,PBM file" % filename



