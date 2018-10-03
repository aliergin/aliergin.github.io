#
# This plugin identify a GIF file and returns the size
#

def read_headers(filename):

  h = None
  f = open(filename,'rb')
  if f:
    h = f.read(16)
    f.close()
  return h

def identify(filename):

  h = read_headers(filename)
  if h == None:
    return None

  # This is the GIF header
  if h[:6] in ('GIF87a', 'GIF89a'):
    return ((ord(h[7])<<8 | ord(h[6])),(ord(h[9])<<8 | ord(h[8])))
  return None

if __name__ == "__main__":
    import sys
    import GIF
    
    if len(sys.argv) < 2:
      print 'Usage: %s files...\n' % sys.argv[0]
      sys.exit(0)
        
    for filename in sys.argv[1:]:
        info=GIF.identify(filename)
	if info != None:
	  print "%s (size = %d,%d)" % (filename,info[0],info[1])
	else:
	  print "%s is not a GIF file" % filename


