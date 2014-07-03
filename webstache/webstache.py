#!/usr/bin/env python

import os, sys, getopt, argparse
import glob 
import pystache
import json
from distutils import dir_util

def last(xs):
  return xs[-1]

def first(xs):
  return xs[0]

def removepath(filename):
  return last(os.path.split(filename))

def removetype(filename):
  return first(filename.split("."))

def basename(filename):
  return removetype(removepath(filename))

def loadfile(filename):
  return json.loads(open(filename).read())

def main():
  parser = argparse.ArgumentParser(description='Generates static webpages based off of mustache templates')
  parser.add_argument('directory', nargs='?', default=os.getcwd(), help='Directory of mustache files and data')
  parser.add_argument('-o', '--output', nargs='?', default='out', help='Name of directory to store the output')
  parser.add_argument('-b', '--base', nargs='?', default='base.mustache', help='Name of the file for the base mustache template file')
  parser.add_argument('-m', '--menu', nargs='?', default='menu.mustache', help='Name of the file for the menu mustache template file')
  args = parser.parse_args()
  
  print("Creating webpages from %s" % args.directory)
  base = os.path.join(args.directory, args.base)
  if(not os.path.exists(base)):
      sys.stderr.write("base.mustache not found in %s\n" % args.directory)
      sys.exit(1)

  template_file = open(base, "r")
  template = template_file.read()
  template_file.close()
  data = glob.glob(os.path.join(args.directory, "*.json"))

  static_dir = os.path.join(args.directory, "static")
  
  datafiles = [(basename(file), loadfile(file)) for file in data]

  path = os.path.join(args.directory, args.output)
  if os.path.exists(static_dir):
    dir_util.copy_tree(static_dir, path)
  elif not os.path.exists(path):
    os.mkdir(path)

  for dataname, datafile in datafiles:
    htmlfile = open(os.path.join(path, dataname + ".html"), "w")
    htmlfile.write(pystache.render(template, datafile))
    htmlfile.close()


if __name__ == "__main__":
  main()
