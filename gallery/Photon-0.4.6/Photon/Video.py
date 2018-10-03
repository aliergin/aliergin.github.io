
"""This small library load and identify some image format """

from Photon import QuickTime, AVI
from random import randrange

class Video:
  format = None
  size = (0,0)
  mode = None
  plugin = None
  moviefile = None
  privatedata = None

  def __init__(self):
    pass

  def get_random_frame(self, pictfile):
    frame = randrange(0, self.frames)
    if self.plugin == 'QuickTime':
      return QuickTime.extract_jpeg_file(self.moviefile,
					 self.privatedata,
					 pictfile,
					 frame)
    elif self.plugin == 'AVI':
      return AVI.extract_jpeg_file(self.moviefile,
				   self.privatedata,
				   pictfile,
				   frame)
    else:
      return None


  def get_frame(self, pictfile, frame):
    if self.plugin == 'QuickTime':
      return QuickTime.extract_jpeg_file(self.moviefile,
					 self.privatedata,
					 pictfile,
					 frame)
    elif self.plugin == 'AVI':
      return AVI.extract_jpeg_file(self.moviefile,
	                           self.privatedata,
				   pictfile,
				   frame)
    else:
      return None


def identify(filename):
  info = AVI.identify(filename)
  if info <> None:
    video = Video()
    video.privatedata = info
    video.format = 'AVI (%s)' % info['format']
    video.size = info['video_size']
    video.frames = info['frames']
    video.plugin = 'AVI'
    video.moviefile = filename
    return video

  info = QuickTime.identify(filename)
  if info <> None:
    video = Video()
    video.privatedata = info
    video.format = 'QuickTime (%c%c%c%c)' % (((info['format']>>24)&255),((info['format']>>16)&255),((info['format']>>8)&255),((info['format'])&255))
    video.size = (info['width'] , info['height'])
    video.frames = info['frames']
    video.plugin = 'QuickTime'
    video.moviefile = filename
    return video

  raise IOError("Format not recognized")

if __name__ == "__main__":
    import sys
    import Video
    
    if len(sys.argv) < 2:
      print 'Usage: %s files...\n' % sys.argv[0]
      sys.exit(0)
        
    for filename in sys.argv[1:]:
        im=Video.open(filename)
	if im != None:
	  print "%s (format=%s  size <%dx%d> mode=%s)" % (filename,im.format,im.size[0],im.size[1])
	else:
	  print "%s is not recognized" % filename


