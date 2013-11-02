#! usr/bin/python

"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import argparse, os
from mutagen.mp3 import MP3

# set up command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("source", type=str, help="path to scan for mp3 files to organize and move")
parser.add_argument("dest", type=str, help="destination path for organized mp3 files")
args = parser.parse_args()

#source and destination paths
source = args.source
dest = args.dest

def extract_artist(file):
	"return string of artist name, read from file given as argument"
	my_mp3 = MP3(file)
	artist = str(my_mp3["TPE1"])
	artist = artist.split(b'\0',1)[0] #remove trailing null bytes
	return artist

def extract_album(file):
	"read album tag on an mp3 file and return album name as a string"
	my_mp3 = MP3(file)
	album = str(my_mp3["TALB"])
	album = album.split(b'\0',1)[0] #remove trailing null bytes
	return album
		
def create_tuple_list(source):
	tuple_list = []
	for root, dirs, files in os.walk(os.path.abspath(source)):	
		for name in files:
			if(name.lower().endswith(".mp3")):
				path = os.path.abspath(name)
				filename = name
				artist = extract_artist(path)
				album = extract_album(path)
				my_tuple = (path, filename, artist, album)
				tuple_list.append(my_tuple)
	return tuple_list
	
def move_files(tuple_list):
	for path, filename, artist, album in tuple_list:
		current_source = os.path.abspath(path)
		current_dest_no_filename = os.path.abspath(dest + "/" + artist + "/" + album)
		current_dest = os.path.abspath(dest + "/" + artist + "/" + album + "/" + filename)
		if not os.path.exists(current_dest_no_filename):
			os.makedirs(current_dest_no_filename)
		if not os.path.exists(current_dest):
			os.rename(current_source, current_dest)
			print "moving " + current_source + "\nto " + current_dest + "..."
		else: print current_dest + " already exists. skipping this file..."

#do something
move_files(create_tuple_list(source))
print "done.\n"
# future plans: add options for: verbosity, copy versus just move, scan source directory recursively or just top dir
