#!/usr/bin/env python3

from pyaff4 import data_store
from pyaff4 import aff4_image
from pyaff4 import lexicon
from pyaff4 import rdfvalue
from pyaff4 import zip
from fuse import FUSE, FuseOSError, Operations

import re
import sys
import os
import errno


def extractStream(path):
	# Convert a filename to URN. AFF4 uses URNs to refer to everything. file to be mounted
	volume_path_urn = rdfvalue.URN.NewURNFromFilename(path)

	# We need to make a resolver to hold all the RDF metadata
	resolver = data_store.MemoryDataStore()

	# Open the AFF4 volume from a ZipFile.
	with zip.ZipFile.NewZipFile(resolver,None, volume_path_urn) as volume:
		volume_urn = volume.urn

		# This will dump out the resolver.
		try:
			resolver.Dump()
		except TypeError:
			pass

		# Find all subjects with a type of Image. Alternatively if you
		# know the subject URN in advance just open it. Replace the
		# AFF4_IMAGE_TYPE with AFF4_MAP_TYPE for maps.
		for subject in resolver.QueryPredicateObject(None,
				lexicon.AFF4_TYPE, lexicon.AFF4_IMAGE_TYPE):

			# This should be able to open the URN.
			with resolver.AFF4FactoryOpen(subject) as in_fd:

				# Escape the subject to make something like a valid filename.
				filename = re.sub("[^a-z0-9A-Z-]",
								  lambda m: "%%%02x" % ord(m[0]),
								  str(subject))
				print ("Writing %s to file %s" % (subject, filename))

				while 1:
					data = in_fd.read(1024 * 1024)
					if not data:
						break
				return data.decode('utf-8')


class Passthrough(Operations):
	def __init__(self,root):
		self.root = root
		
	
    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path
		
	# Filesystem methods
    # ==================

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

   

    # File methods
    # ============

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)
		
		
#Program execution starts here
def main(mountpoint, root):
	if len(sys.argv) < 2:
        sys.exit("No file provided.")
    elif len(sys.argv) < 3:
        sys.exit("No mount directory specified.")
    else:
		imagestream = extractStream(root)
		FUSE(Passthrough(imagestream), mountpoint,nothreads=True, foreground=True)


if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])
