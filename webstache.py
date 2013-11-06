#!/usr/bin/python

import os, sys, getopt, argparse
import glob
import pystache
import json

def main():
  parser = argparse.ArgumentParser(description='Generates static webpages based off of mustache templates')
  parser.add_argument('directory', nargs='?', default=os.getcwd(), help='Directory of mustache files and data')
  parser.add_argument('-o', '--output', nargs='?', default='output', help='Name of directory to store the output')
  args = parser.parse_args()
  
  print("Creating webpages from " + args.directory)
  template_file = open(args.directory + "/base.mustache", "r")
  template = template_file.read()
  data = glob.glob(args.directory + "/*.json")

  dataname = []
  datafiles = []
  for file in data:
    dataname.append(os.path.split(file)[-1].split(".")[0])
    currfile = open(file).read()
    datafiles.append(json.loads(currfile))

  path = os.path.join(args.directory, args.output)
  if not os.path.exists(path):
    os.mkdir(path)

  i = 0
  while i < len(datafiles):
    htmlfile = open(os.path.join(path, dataname[i] + ".html"), "w")
    htmlfile.write(pystache.render(template, datafiles[i]))
    i += 1


if __name__ == "__main__":
  main()
