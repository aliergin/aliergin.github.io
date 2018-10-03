#
# This plugin identify a PNG file and returns the size
#

def read_headers(filename):

  h = None
  f = open(filename,'rb')
  if f:
    h = f.read(32)
    f.close()
  return h

def identify(filename):

  h = read_headers(filename)
  if h == None:
    return None

  # This is the PNG header
  if h[:8] == '\x89PNG\r\n\x1a\n':
    w = ord(h[16])<<24 | ord(h[17])<<16 | ord(h[18])<<8 | ord(h[19]) 
    h = ord(h[20])<<24 | ord(h[21])<<16 | ord(h[22])<<8 | ord(h[23]) 
    return (w,h)
  return None

if __name__ == "__main__":
    import sys
    import PNG
    
    if len(sys.argv) < 2:
      print 'Usage: %s files...\n' % sys.argv[0]
      sys.exit(0)
        
    for filename in sys.argv[1:]:
        info=PNG.identify(filename)
	if info != None:
	  print "%s (size = %d,%d)" % (filename,info[0],info[1])
	else:
	  print "%s is not a PNG file" % filename


