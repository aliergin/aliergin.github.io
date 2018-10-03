
"""This small library load and identify some image format """

from Photon import JPEG,GIF,PNG, PxM

class Image:
  format = None
  size = (0,0)
  mode = None

def open(filename):
  im = Image()
  size = JPEG.identify(filename)
  if size <> None:
    im.format = 'JPEG'
    im.size = size
    return im
  size = GIF.identify(filename)
  if size <> None:
    im.format = 'GIF'
    im.size = size
    im.mode = 'P'
    return im
  size = PNG.identify(filename)
  if size <> None:
    im.format = 'PNG'
    im.size = size
    return im
  (format, size) = PxM.identify(filename)
  if size <> None:
    im.format = format
    im.size = size
    return im

  raise IOError("Format not recognized")

if __name__ == "__main__":
    import sys
    import Image
    
    if len(sys.argv) < 2:
      print 'Usage: %s files...\n' % sys.argv[0]
      sys.exit(0)
        
    for filename in sys.argv[1:]:
        im=Image.open(filename)
	if im != None:
	  print "%s (format=%s  size <%dx%d> mode=%s)" % (filename,im.format,im.size[0],im.size[1],im.mode)
	else:
	  print "%s is not recognized" % filename


