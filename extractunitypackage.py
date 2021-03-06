#!/usr/bin/env python
#
# UnityPackage Extractor
#
# Extracts files/folders from a .unitypackage file, reading the 'pathname'
# files it contains to rebuild a "readable" file/folder structure.
#
# Usage: extractunitypackage.py input_file [output_path]
#
# "input_file" should be a .unitypackage file. The part of the filename
# before the extension will be used as the name of the directory that the 
# packages contents will be extracted to.
#
# "output_path" is an optional path where the package's files will be
# extracted to. If omitted, the current working directory is used. If
# specified, the path should already exist.

# Update (by Entwicklerpages): Simple fixes for python3 support. Now works on both versions.

import os
import stat
import shutil
import sys
import tarfile

def extractunitypackage(inputFile, outputDir):
	workingDir = os.path.join('.', '.working')

	# can't proceed if the output dir exists already
	# but if the temp working dir exists, we clean it out before extracting
	if os.path.exists(outputDir):
		print ('Output dir "' + outputDir + '" exists. Aborting.')
		return
	if os.path.exists(workingDir):
		shutil.rmtree(workingDir)

	# extract .unitypackage contents to a temporary space
	tar = tarfile.open(inputFile, 'r:gz')
	tar.extractall(workingDir);
	tar.close()


	os.makedirs(outputDir)


	# build association between the unitypackage's root directory names
	# (which each have 1 asset in them) to the actual filename (stored in the 'pathname' file)
	mapping = {}
	for i in os.listdir(workingDir):
		rootFile = os.path.join(workingDir, i)
		asset = i

		if os.path.isdir(rootFile):
			realPath = ''

			# we need to check if an 'asset' file exists (sometimes it won't be there
			# such as when the 'pathname' file is just specifying a directory)
			hasAsset = False
			hasMeta = False

			for j in os.listdir(rootFile):
				# grab the real path
				if j == 'pathname':
					lines = [line.strip() for line in open(os.path.join(rootFile, j))]
					realPath = os.path.normpath(lines[0])     # should always be on the first line
				elif j == 'asset':
					hasAsset = True
				elif j == 'asset.meta':
					hasMeta = True

			# if an 'asset' file exists in this directory, then this directory
			# contains a file that should be moved+renamed. otherwise we can
			# ignore this directory altogether...
			if hasAsset or hasMeta:
				path, filename = os.path.split(realPath)

				destDir = os.path.join(outputDir, path)
				if not os.path.exists(destDir):
					os.makedirs(destDir)

				if hasAsset:
					destFile = os.path.join(destDir, filename)
					source = os.path.join(workingDir, asset, 'asset');
					print ('Move ' + source + ' => ' + destFile)
					shutil.move(source, destFile)
					# change file permissions for unix because under mac os x
					# (perhaps also other unix systems) all files are marked as executable
					# for safety reasons os x prevent the access to the extracted files
					os.chmod(destFile, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

				if hasMeta:
					destFileMeta = os.path.join(destDir, filename + '.meta')
					sourceMeta = os.path.join(workingDir, asset, 'asset.meta');
					print ('Move ' + sourceMeta + ' => ' + destFileMeta)
					shutil.move(sourceMeta, destFileMeta)
					# change file permissions for unix because under mac os x
					# (perhaps also other unix systems) all files are marked as executable
					# for safety reasons os x prevent the access to the extracted files
					os.chmod(destFileMeta, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

				print (asset + ' => ' + realPath)

	# done, cleanup any leftovers...
	shutil.rmtree(workingDir)


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print ('No input file specified.')
		sys.exit()

	name, extension = os.path.splitext(os.path.basename(sys.argv[1]))

	outputDir = ''
	if len(sys.argv) > 2:
		outputDir = sys.argv[2]
	else:
		outputDir = os.path.join('.', name)

	extractunitypackage(sys.argv[1], outputDir)
