
#
# http://www.funducode.com/freec/Fileformats/format3/format3b.htm
#

def read_headers(filename,size=65536):

  h = None
  f = open(filename,'rb')
  if f:
    h = f.read(size)
    f.close()
  return h

def identify(filename):

  # I've some photos made from a pentax that store the thumbnail at the beginning
  size = 65536
  while True:
    try:
      h = read_headers(filename,size)
      if h == None:
	return None

      # This is the JPEG/JFIF header
      if h[0:2] == '\xff\xd8':
	return find_marker_SOFx(h[2:])
      return None
    except IndexError, err:
      size = size * 2
      print "Jpeg Resize and reload header ",size
      if size > 1048576:
	print "Can't identify this file as an JPEG file %s" % filename
      	return None


def find_marker_SOFx(h):

  i=0

  while 1:
    # Hum, this is not a valid chunk
    if h[i] != "\xff":
      return None
    i+=1

    # Skip any padding ff byte (this normal)
    while h[i] == 0xff:
      i+=1

    # All SOF0 to SOF15 is valid (for me) not sure
    #print "Found marker %2.2x at index %d"% (ord(h[i]),i)
    if h[i] >= '\xc0' and h[i]<='\xcf' and h[i]!='\xc4' and h[i]!='\xcc':
      i+=1
      return ((ord(h[i+5])<<8 | ord(h[i+6])),(ord(h[i+3])<<8 | ord(h[i+4])))
    i+=1
  
    # Skip to next marker
    i+= ord(h[i])<<8 | ord(h[i+1])
    #print "New offset at " , i

if __name__ == "__main__":
#   import profile
#   profile.run('main()')
    import sys
    import JPEG
    
    if len(sys.argv) < 2:
      print 'Usage: %s files...\n' % sys.argv[0]
      sys.exit(0)
        
    for filename in sys.argv[1:]:
        info=JPEG.identify(filename)
	if info != None:
	  print "%s (size = %d,%d)" % (filename,info[0],info[1])
	else:
	  print "%s is not a Jpeg file" % filename



