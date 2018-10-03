#
# Parse a QuickTime movie file produced by many digital camera
#
# http://developer.apple.com/documentation/QuickTime/QTFF/
# QuickTime is trademark of Apple
#

import struct
from random import randrange

quicktime_verbose = 0
 
def read_headers(filename,size=65536):

  h = None
  f = open(filename,'rb')
  if f:
    h = f.read(size)
    f.close()
  return h

def open_atom(filename):
  f = open(filename,'rb')
  if f:
    return f
  return None

def close_atom(f):
  f.close()

def read_atom(f):
  h = f.read(8)
  if len(h) < 8:
    return None
  atom = {}
  s = struct.unpack(">L", h[0:4])
  if s[0] < 8:
    return None
  atom['size'] = s[0] - 8
  atom['type'] = h[4:8]
  atom['offset'] = f.tell()
  #atom['data'] = f.read(atom['size'] - 8)
  return atom

def parse_PICT(f, atom):
  print "PICT size:%d " % atom['size']
  atom['data'] = f.read(atom['size'])
  f.seek(-atom['size'],1)
  return 1

def parse_stbl(f, node, info):
  begin = f.tell()
  current = 0
  while current < node['size']:
    atom = read_atom(f)
    if atom == None:
      break
    current += atom['size'] + 8
    if atom['type'] == 'stsd':
      parse_stsd(f, atom, info)
    elif atom['type'] == 'stsz':
      parse_stsz(f, atom, info)
    elif atom['type'] == 'stco':
      parse_stco(f, atom, info)
    elif atom['type'] == 'stsc':
      parse_stsc(f, atom, info)
    else:
      f.seek(atom['size'],1)
  f.seek(begin,0)

def parse_stsd(f, atom, info):
  data = f.read(atom['size'])
  (version, flags0, flags1, flags2, entries) = struct.unpack(">B3BL", data[0:8])
  i = 8
  while entries:
    (size, format, refindex) = struct.unpack(">LL6xH", data[i:i+16])
    #print "size:%d format:%c%c%c%c refindex=%d" % (size, format>>24, (format>>16)&255, (format>>8)&255, format&255, refindex)
    if info.has_key('format'):
      print "Warning i found severall different format, is it correct. Please send your video to the author"
      return
    info['format'] = format
    (width, height) = struct.unpack(">HH", data[i+32:i+36])
    info['width'] = width
    info['height'] = height
    i+=size
    entries-=1

def parse_stsc(f, atom, info):
  data = f.read(atom['size'])
  (version, entries) = struct.unpack(">B3xL", data[0:8])
  if quicktime_verbose>0:
    print "stsc entries: %d" % (entries)
  i = 8
  while entries:
    (firstchunk, sampleperchunk, sampleid) = struct.unpack(">LLL", data[i:i+12])
    if quicktime_verbose>1:
      print "firstchunk=%d sampleperchunk=%d sampleid=%d" % (firstchunk, sampleperchunk, sampleid)
    firstchunk-=1
    info['chunk_info'].append((firstchunk, sampleperchunk))
    i+=12
    entries-=1


def parse_stsz(f, atom, info):
  data = f.read(atom['size'])
  (version, defsize, entries) = struct.unpack(">B3xLL", data[0:12])
  if quicktime_verbose>0:
    print "stsz frames: %d" % (entries)
  info['frames'] = entries
  info['sample_size'] = struct.unpack(">%dL" % entries , data[12:])

def parse_stco(f, atom, info):
  data = f.read(atom['size'])
  (version, entries) = struct.unpack(">B3xL", data[0:8])
  if quicktime_verbose>0:
    print "stco entries: %d" % (entries)
  info['chunks'] = entries
  info['chunk_offset'] = struct.unpack(">%dL" % entries , data[8:])


#
# Parse an atom an recurse if this atom contains other atoms
# This is very small parser, so we didn't try to parse every track
# We stop after found the first video track
#
def parse_moov(f, parent, info):
  begin = f.tell()
  current = 0
  while current < parent['size']:
    atom = read_atom(f)
    if atom == None:
      break
    if quicktime_verbose>0:
      print "+ %s" % atom['type']
    # Yes we have found a vmhd chunk, so this movie have a video track
    if atom['type'] == 'vmhd':
      info['video_chunk'] = parent
    if info['video_chunk'] != None and info['video_chunk'] == parent:
      if atom['type'] == 'stbl':
      	parse_stbl(f, parent, info)
    if atom['type'] in ('mdia', 'mvhd', 'trak', 'minf', 'mdhd', 'hdlr', 'stbl'):
      parse_moov(f, atom, info)
    current += atom['size'] + 8
    f.seek(atom['size'],1)
  f.seek(begin,0)

def parse_atom(f, parent, prefix):
  begin = f.tell()
  current = 0
  while current < parent['size']:
    atom = read_atom(f)
    if atom == None:
      break
    print "%s \"%s\" (size=%d)" % (prefix, atom['type'], atom['size'])
    if atom['type'] in ('mdia', 'mvhd', 'trak', 'minf', 'mdhd', 'hdlr', 'stbl'):
      parse_atom(f, atom, prefix + '+')
    current += atom['size'] + 8
    f.seek(atom['size'],1)
  f.seek(begin,0)

def extract_jpeg_files(moviefile, info, basename="/tmp/photon%8.8d.jpg"):

  f = open_atom(moviefile)
  frame = 0
  for chunk in range(info['chunks']):
    if quicktime_verbose>1:
      print "chunks: %d   => offset: %d" % (chunk, info['chunk_offset'][chunk])
    f.seek(info['chunk_offset'][chunk],0)
    samplesbychunk = -1
    for chunk_info in info['chunk_info']:
      if chunk_info[0] <= chunk:
	samplesbychunk = chunk_info[1]
      else:
	pass
    for jjj in range(samplesbychunk):
      size = info['sample_size'][frame]
      out = open(basename % frame, "wb");
      h = f.read(2)
      if h[0:2] == '\xff\xd8':
	out.write(h)
	out.write(f.read(size-2))
      else:
        print "Warning this is not a jpeg file (frame=%d)" % frame
      out.close()
      frame+=1

#
# Extract one image from the file
#
def extract_jpeg_file(moviefile, info, outfile, frame):

  f = open_atom(moviefile)
  # Calculate the offset for our image
  chunk_group = 0
  chunk_frame_start = 0
  chunk_frame_end = 0
  chunk_frames = 0
  for chunk_info in info['chunk_info']:
    if chunk_frames == 0:
      chunk_group = chunk_info[0]
      chunk_frames = chunk_info[1]
    else:
      chunk_frame_end = chunk_frame_start + (chunk_info[0] - chunk_group) * chunk_frames
      if frame >= chunk_frame_start and frame < chunk_frame_end:
	break
      chunk_frame_start = chunk_frame_end
      chunk_group = chunk_info[0]
      chunk_frames = chunk_info[1]
  (chunk, offimg) = divmod(frame - chunk_frame_start, chunk_frames)
  chunk += chunk_group
  if quicktime_verbose>1:
    print "%4.4d |  chunk=%d /// offimg=%d" % (frame, chunk, offimg)

  offset = info['chunk_offset'][chunk]
  for j in xrange(offimg):
    offset += info['sample_size'][frame-j-1]
  # Go to the beginning of the image
  f.seek(offset,0)
  size = info['sample_size'][frame]
  out = open(outfile, "wb")
  h = f.read(2)
  if h[0:2] == '\xff\xd8':	# To be sure that we extract a Jpeg file
    out.write(h)
    out.write(f.read(size-2))
  else:
    print "Warning: this is not a jpeg file (frame=%d)" % frame
  #out.write(f.read(size))
  out.close()
  close_atom(f)
  

def __identify(filename):

  if struct.calcsize(">L") != 4:
    print "A long is not equal to 4 bytes with your python installation. Abording"
    return None

  h = read_headers(filename,12)
  if h == None:
    return None

  # is this a QuickTime file ?
  if h[4:8] not in ('pnot', 'moov', 'mdat'):
    return None

  # Parse the file into atom (chunk), and try to find a 
  # mdat and moov chunk
  f = open_atom(filename)
  found_mdat = found_moov = 0
  info = {}
  info['chunk_info'] = list()
  while True:
    atom = read_atom(f)
    if atom == None:
      break
    #print "Found a new atom \"%s\" (size=%d)" % (atom['type'], atom['size'])
    if atom['type'] in ('pnot', 'PICT'):
      pass
    elif atom['type'] == 'mdat':
      found_mdat = 1
      info['mdat_offset'] = f.tell()
    elif atom['type'] == 'moov':
      found_moov = 1
      info['video_chunk'] = None
      parse_moov(f, atom, info)
      if quicktime_verbose>0:
      	parse_atom(f, atom, "+")
      
    else:
      print "Abording unknow Atom type"
      #break
    f.seek(atom['size'],1)

  close_atom(f)

  if not (found_moov and found_mdat):
    return None

  if not info.has_key('format'):
    return None

  if info['format'] == 0x6a706567:	# 'jpeg'
    #print "It's a jpeg movie"
    return info
  return None

def identify(filename):
  return __identify(filename)

def extract_random_picture(moviefile, pictfile):
  video = __identify(moviefile)
  if video == None:
    return None
  r = randrange(0, video['frames'])
  extract_jpeg_file(moviefile, video, pictfile, r)
  return True

def extract_picture(moviefile, pictfile, frame):
  video = __identify(moviefile)
  if video == None:
    return None
  extract_jpeg_file(moviefile, video, pictfile, frame)
  return True



if __name__ == "__main__":
    import sys
    import QuickTime
    
    if len(sys.argv) < 2:
      print 'Usage: %s files...\n' % sys.argv[0]
      sys.exit(0)
        
    for filename in sys.argv[1:]:
        info=QuickTime.identify(filename)
	if info != None:
	  print "%s (format='%x', frames='%d')" % (filename,info['format'],info['frames'])
	  #extract_jpeg_files(filename, info)
  	  for frame in xrange(info['frames']):
	  #for frame in xrange(1138,1142):
	    extract_jpeg_file(filename, info, "/tmp/photon%8.8d.jpg" % frame, frame)
	else:
	  print "%s is not a Quicktime movie file" % filename



