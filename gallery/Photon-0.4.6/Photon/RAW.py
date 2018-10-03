#
# This plugin identify, convert a raw image produce by a digital camera
# To do the job, we use the dcraw program, exiftool, and any ppm2xxx program
#

import os, string, commands, popen2

class RAW:

  format = None

  def __init__(self):
    pass

  def convert(self, outputfilename):

    dcrawcmd = "dcraw -w -c \"%s\" > \"%s\"" % (self.filename, outputfilename)
    status , resultstring = commands.getstatusoutput(dcrawcmd)
    if status != 0:
      print "ERROR: dcraw can not convert the image into a PPM file (err=%d)" % status
      print "dcraw output:"
      print resultstring
      return None
    return 1

#    ppmformat = None
#    linecounter = 0
#    dcrawcmd = "dcraw -w -2 -c \"%s\"" % self.filename
#    handle = Popen3(dcrawcmd, False)
#    while handle.poll() == -1:
#      line = self.fromchild.readline()
#      if linecounter == 0:	# First line is always the format
#	if line <> 'P6':
#	  raise IOError("Format not recognized \"%\"" % line)
#	linecounter+=1
#      elif linecounter == 1:	# Second line is the size of the image
#	size=string.split(line," ")
#	print "Raw image size %dx%d" % size
#	linecounter+=1
#      elif linecounter == 2: 	# Third line precise the max value for a color (255 or 65535)
#	maxvalue=int(line)
#	linecounter+=1
#      else:


    
    pass


  
def identify(filename):

  # Try to identify the image using dcraw
  dcrawcmd = "dcraw -i \"%s\"" % filename
  status , resultstring = commands.getstatusoutput(dcrawcmd)
  if status != 0:
    print "ERROR: dcraw does not recognize the image (err=%d)" % status
    print "dcraw output:"
    print resultstring
    return None
  # Get the image format
  idx = string.rfind(resultstring," is a ")
  if idx < 0:
    print "ERROR: Strange the string doesn't contains the magic string."
    print resultstring
    return None
  
  # All string finish by a " image."
  format = resultstring[idx+6:-8]
  raw = RAW()
  raw.format = format
  raw.filename = filename
  
  return raw

  

if __name__ == "__main__":
    import sys
    import RAW
    
    if len(sys.argv) < 2:
      print 'Usage: %s files...\n' % sys.argv[0]
      sys.exit(0)
        
    for filename in sys.argv[1:]:
        info=RAW.identify(filename)
	if info != None:
	  print "%s (format = %s)" % (filename,info.format)
	else:
	  print "%s is not a RAW file" % filename


