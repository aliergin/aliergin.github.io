#!/usr/bin/env python

import sys, glob
assert sys.version >= '2', "Install Python 2.0 or greater"
try:
  from distutils.core import setup
except ImportError:
  raise SystemExit, "Photon requires distutils to build and install. Perhaps you need to install python-devel ?"

import Photon

# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
if sys.version < '2.2.3':
  from distutils.dist import DistributionMetadata
  DistributionMetadata.classifiers = None
  DistributionMetadata.download_url = None

DESCRIPTION="""Photon is a photo album with a clean design.
Features:
* static HTML pages (you can put all pages and images on a CD-ROM)
* slideshow (use javascript optional)
* can use gimp to resize picture
* navigation between the image can use the keyboard (use javascript optional)
* works in any browser (Mozilla, Netscape Navigator 4.x, Konqueror, Opera)
* Each image can have a comment (with HTML tags)
* Information about the image (if taken from a digital picture) can be draw
* thumbnail image size can be choosen by the user
* output images can be scalled down
* movie support
* control the number of thumbnail in a page."""

setup(name="Photon",
      version=Photon.version,
      author="Luc Saillard",
      author_email="luc@saillard.org",
      url="http://www.saillard.org/photon/",
      description="Photon is a static HTML gallery generator",
      long_description=DESCRIPTION,
      
      license = "GNU GPL v2",

      packages=['Photon'],
      
      scripts=['photon'],

      data_files=[('share/photon/images', glob.glob('images/*.gif')+
	                                   glob.glob('images/*.png')),
                  ('share/photon/templates/photonv1', glob.glob('templates/photonv1/*'))
		 ]
     )

