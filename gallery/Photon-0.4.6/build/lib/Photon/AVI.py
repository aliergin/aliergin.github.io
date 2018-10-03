#
# Parse a AVI movie file produced by many digital camera
#
#

import struct, array
from random import randrange

avi_verbose = 0

huffman_table = array.array('c',  
	"\xFF\xC4\x01\xA2\x00\x00\x01\x05\x01\x01\x01\x01"\
        "\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02"\
        "\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x01\x00\x03"\
        "\x01\x01\x01\x01\x01\x01\x01\x01\x01\x00\x00\x00"\
        "\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"\
        "\x0A\x0B\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05"\
        "\x05\x04\x04\x00\x00\x01\x7D\x01\x02\x03\x00\x04"\
        "\x11\x05\x12\x21\x31\x41\x06\x13\x51\x61\x07\x22"\
        "\x71\x14\x32\x81\x91\xA1\x08\x23\x42\xB1\xC1\x15"\
        "\x52\xD1\xF0\x24\x33\x62\x72\x82\x09\x0A\x16\x17"\
        "\x18\x19\x1A\x25\x26\x27\x28\x29\x2A\x34\x35\x36"\
        "\x37\x38\x39\x3A\x43\x44\x45\x46\x47\x48\x49\x4A"\
        "\x53\x54\x55\x56\x57\x58\x59\x5A\x63\x64\x65\x66"\
        "\x67\x68\x69\x6A\x73\x74\x75\x76\x77\x78\x79\x7A"\
        "\x83\x84\x85\x86\x87\x88\x89\x8A\x92\x93\x94\x95"\
        "\x96\x97\x98\x99\x9A\xA2\xA3\xA4\xA5\xA6\xA7\xA8"\
        "\xA9\xAA\xB2\xB3\xB4\xB5\xB6\xB7\xB8\xB9\xBA\xC2"\
        "\xC3\xC4\xC5\xC6\xC7\xC8\xC9\xCA\xD2\xD3\xD4\xD5"\
        "\xD6\xD7\xD8\xD9\xDA\xE1\xE2\xE3\xE4\xE5\xE6\xE7"\
        "\xE8\xE9\xEA\xF1\xF2\xF3\xF4\xF5\xF6\xF7\xF8\xF9"\
        "\xFA\x11\x00\x02\x01\x02\x04\x04\x03\x04\x07\x05"\
        "\x04\x04\x00\x01\x02\x77\x00\x01\x02\x03\x11\x04"\
        "\x05\x21\x31\x06\x12\x41\x51\x07\x61\x71\x13\x22"\
        "\x32\x81\x08\x14\x42\x91\xA1\xB1\xC1\x09\x23\x33"\
        "\x52\xF0\x15\x62\x72\xD1\x0A\x16\x24\x34\xE1\x25"\
        "\xF1\x17\x18\x19\x1A\x26\x27\x28\x29\x2A\x35\x36"\
        "\x37\x38\x39\x3A\x43\x44\x45\x46\x47\x48\x49\x4A"\
        "\x53\x54\x55\x56\x57\x58\x59\x5A\x63\x64\x65\x66"\
        "\x67\x68\x69\x6A\x73\x74\x75\x76\x77\x78\x79\x7A"\
        "\x82\x83\x84\x85\x86\x87\x88\x89\x8A\x92\x93\x94"\
        "\x95\x96\x97\x98\x99\x9A\xA2\xA3\xA4\xA5\xA6\xA7"\
        "\xA8\xA9\xAA\xB2\xB3\xB4\xB5\xB6\xB7\xB8\xB9\xBA"\
        "\xC2\xC3\xC4\xC5\xC6\xC7\xC8\xC9\xCA\xD2\xD3\xD4"\
        "\xD5\xD6\xD7\xD8\xD9\xDA\xE2\xE3\xE4\xE5\xE6\xE7"\
        "\xE8\xE9\xEA\xF2\xF3\xF4\xF5\xF6\xF7\xF8\xF9\xFA" )
 
def read_headers(filename,size=65536):
  h = None
  f = open(filename,'rb')
  if f:
    h = f.read(size)
  return (f, h)

def read_le32(f):
  h = f.read(4)
  s = struct.unpack("<L", h)
  return s[0]

def build_cache(f, info):

    f.seek(info['movie_start'], 0)
    info['frames_offsets'] = []
    n_frame_data = 0

    while n_frame_data<info['frames']:
      tag = f.read(4)
      if len(tag)<4:
	return None
      tag_size = read_le32(f)

      if tag == '00dc': # If more than one stream, i'll be in trouble
	info['frames_offsets'].append((f.tell(), tag_size))
	n_frame_data+=1
      elif tag == '01wb':
	# audio
	pass
      elif tag == 'idx1':
	# This is an optional index, for the moment, it is not used
        break
      else:
	print "Unknown chunk ID ", tag

      f.seek(tag_size, 1)
    if avi_verbose>1:
      print "Total number of frames: %d" % (info['frames'])
      print "Total read: %d" % n_frame_data

#
# Some AVI have an index to frame, at the end of the file. This can speed up a
# lot, when doing fast forward/backward. But sometimes, the pos is not from the
# beginning of the file, but from the start of the movie
# 
def read_idx(f, info, size):

  info['frames_offsets'] = []
  n = size/16
  if n<1:
    return None

  while n:
    tag = f.read(4)
    flags = read_le32(f)
    pos = read_le32(f)
    len = read_le32(f)
    if tag == '00dc':
      info['frames_offsets'].append(pos, len)
    #print "Tag: %s; flags=%8.8x;   pos=%8d;   len=%8d" % (tag, flags, pos, len)
    n-=1
    
  return 1


#
# Is this file have an index ?, so loaded
#
def find_n_read_idx(f, info):

  f.seek(12, 0)
  while True:
    tag = f.read(4)
    if len(tag)<4:
      return None
    tag_size = read_le32(f)

    #print "Tag: %s (len=%8d)" % (tag, tag_size)
    if tag == 'idx1':
      return read_idx(f, info, tag_size)
    else:
      if tag_size&1:
	tag_size+=1
      f.seek(tag_size, 1)
  return None


#
# Copy the Jpeg data from the stream to out
# In MJPEG, many stream don't include the huffman table.
# We need to parse the JPEG stream header to find if we need to add a default huffman table.
#
def fix_n_output_jpeg(h, out):

  has_huffmantable = 0
  i = 2
  while True:

    # Hum, this is not a valid chunk
    if h[i] != "\xff":
      return None
    i+=1

    # Skip any padding ff byte (this normal)
    while h[i] == 0xff:
      i+=1

    # All SOF0 to SOF15 is valid (for me) not sure
    #print "Found marker %2.2x at index %d"% (ord(h[i]),i)
    if h[i] =='\xc4':
      has_huffmantable = 1
    if h[i] == '\xda':
      # Need to flush all the file
      if has_huffmantable:
	out.write(h)
      else:
	out.write(h[0:i-1])
	out.write(huffman_table)
	out.write(h[i-1:])
      return
    i+=1
  
    # Skip to next marker
    s = struct.unpack(">H", h[i:i+2])
    i += s[0]
 




#
# Extract one image from the file
#
def extract_jpeg_file(moviefile, info, outfile, frame):

  f = open(moviefile, 'rb')

  # Build a cache
  if not info.has_key('frames_offsets'):
    build_cache(f, info)

  # Seek and copy the frame data into the file
  try:
    (offset, size) = info['frames_offsets'][frame]
  except IndexError:
    print "Warning: trying to grab frame %d but this frame is not found in the movie" % frame
    print "Perhaps, the file is too short"
    (offset, size) = info['frames_offsets'][len(info['frames_offsets'])-1]

  f.seek(offset,0)
  out = open(outfile, "wb")
  h = f.read(size)
  f.close()
  if h[0:2] == '\xff\xd8':	# To be sure that we extract a Jpeg file
    fix_n_output_jpeg(h, out)
  else:
    print "Warning: this is not a jpeg file (frame=%d)" % frame
  out.close()
  

def __identify(filename):

  if struct.calcsize(">L") != 4:
    print "A long is not equal to 4 bytes with your python installation. Abording"
    return None

  f, h = read_headers(filename,12)
  if h == None:
    return None

  if h[0:4] != 'RIFF':	# RIFF header
    return None
  # 4-8 Filesize
  if h[8:12] != 'AVI ': # Avi chunk
    return None

  info = {}
  stream_index = -1 # Current Stream Header currently parsing [0...n_streams]
  us_frame = 0
  current_codec_type = None
  video_codec = None
  info['video_size'] = (0,0)
  info['frames'] = 0
  info['format'] = None

  while True:
    tag = f.read(4)
    if len(tag)<4:
      return None
    tag_size = read_le32(f)

    if avi_verbose>0:
      print "Tag \"%s\" length=%d" % (tag, tag_size)

    if tag == 'LIST':
      if avi_verbose>0:
	print "Type LIST"
      stag = f.read(4)

      if stag == 'movi':
	info['movie_end'] = f.tell() + tag_size - 4
	info['movie_start'] = f.tell()
	if avi_verbose>0:
	  print " movie_end at %d" % info['movie_end']
	break
      else:
	if avi_verbose>0:
	  print "  ignoring unknown subtag ", stag
	  #f.seek(tag_size-4, 1)

    elif tag == 'avih':
      if avi_verbose>0:
	print "Type AVI header"
      us_frame = read_le32(f)	# in  microsecond
      bit_rate = read_le32(f) * 8
      pad_gran = read_le32(f)
      flags = read_le32(f)
      info['frames'] = read_le32(f)
      init_frames = read_le32(f)
      n_streams = read_le32(f)
      f.seek(tag_size-7*4, 1)

      if avi_verbose>0:
	print "  us_frame = %d" % us_frame
	print "  bit_rate     = %d" % bit_rate
	print "  flags        = %x" % flags
	print "  total frames = %d" % info['frames']
	print "  init_frames  = %d" % init_frames
	print "  n_streams    = %d" % n_streams

    elif tag == 'strh':
      if avi_verbose>0:
	print "Type Stream Header"
      stream_index+=1
      stag = f.read(4)
      if stag == "vids":
	if avi_verbose>0:
	  print "  subtag 'vids'"

	current_codec_type = "VIDEO"
	codec_tag = f.read(4)
	flags =  read_le32(f)
	priority_n_language = read_le32(f)
	inital_frame = read_le32(f)
	scale= read_le32(f)
	rate= read_le32(f)

	if scale and rate:
	  frame_rate = rate
	  frame_rate_base = scale
	elif us_frame:
	  frame_rate = 1000000
	  frame_rate_base = us_frame
	else:
	  frame_rate = 25
	  frame_rate_base = 1
	f.seek(tag_size-7*4, 1)

	if avi_verbose>0:
	  print "  codec_tag = ", codec_tag
	  print "  flags     = %x" % flags
	  print "  scale     = %d" % scale
	  print "  rate      = %d" % rate
	  print "  frame_rate = %d  /  frame_rate_base = %d" % (frame_rate, frame_rate_base)

	# Only mjpeg is supported
	if codec_tag != 'mjpg':
	  return None

      elif stag == "auds":

	if avi_verbose>0:
	  print "  subtag 'auds'"
	current_codec_type = "AUDIO"
	f.seek(tag_size-4, 1)

      else:
	if avi_verbose>0:
	  print "Unknown subtag %s for type 'strh'" % stag
	return None
 
    elif tag == 'strf':

      if current_codec_type == "VIDEO":
        stream_length = read_le32(f)
	stream_width = read_le32(f)
	stream_height = read_le32(f)
	f.seek(4, 1)
	video_codec = f.read(4)
	#f.seek(5*4, 1)
	#video_extra_huffmantable = f.read(tag_size - 10*4)
	f.seek(tag_size-5*4, 1)
	info['video_size'] = (stream_width, stream_height)

	if avi_verbose>0:
	  print "  stream_length = %d" % stream_length
	  print "  stream size = %dx%d" % info['video_size']
	  print "  Video Codec = %s" % video_codec

      elif current_codec_type == "AUDIO":
	f.seek(tag_size, 1)

      else:
	if avi_verbose>0:
	  print "Unknown codec_type for Stream Format"
	return None

    else:
      if avi_verbose>0:
	print "Unknow header ", tag
      if tag_size&1:
	tag_size+=1
      f.seek(tag_size,1)

  f.close()

  if video_codec == "MJPG":
    info['format'] = "MJPG"
    return info
  print "video_codec: ", video_codec
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
    import AVI
    
    if len(sys.argv) < 2:
      print 'Usage: %s files...\n' % sys.argv[0]
      sys.exit(0)
        
    for filename in sys.argv[1:]:
        info=AVI.identify(filename)
	if info != None:
	  print "%s (format='%s', frames='%d')" % (filename,info['format'],info['frames'])
  	  for frame in xrange(info['frames']):
	    extract_jpeg_file(filename, info, "/tmp/photon%8.8d.jpg" % frame, frame)
	else:
	  print "%s is not a AVI movie file" % filename



