# UnityPackage Extractor

Extracts files/folders from a .unitypackage file, reading the 'pathname'
files it contains to build a "readable" file/folder structure which all
the files will be extracted and renamed to match.

## Not original author

Originally forked from @hymerman, and @gered before that. Thanks for the
handy script. I'll be pushing additional tool updates when able.

## Usage

	extractunitypackage.py input_file [output_path]

**input_file** should be a .unitypackage file. The part of the filename
before the extension will be used as the name of the directory that the 
packages contents will be extracted to.

**output_path** is an optional path where the package's files will be
extracted to. If omitted, the current working directory is used. If
specified, the path should already exist.

## Disclaimer

This is a pretty bare-bones script which does a very, very minimal
amount of error checking. I take no responsibility if you lose files,
your computer blows up, etc, as a result of using this script.

