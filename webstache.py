#!/usr/bin/python

import os, sys, getopt, argparse
import glob
import pystache
import json

def main():
  parser = argparse.ArgumentParser(description='Generates static webpages based off of mustache templates')
  parser.add_argument('directory', nargs='?', default=os.getcwd(), help='Directory of mustache files and data')
  args = parser.parse_args()
  
  print(args.directory)
  template_file = open(args.directory + "/base.mustache", "r")
  template = template_file.read()
  data = glob.glob(args.directory + "/*.json")

  print(data)

  dataname = []
  datafiles = []
  for file in data:
    dataname.append(os.path.split(file)[-1].split(".")[0])
    currfile = open(file).read()
    datafiles.append(json.loads(currfile))

  print(dataname)

  if not os.path.exists(args.directory + "/output"):
    os.mkdir(args.directory + "/output")

  i = 0
  while i < len(datafiles):
    htmlfile = open(args.directory + "/output/" + dataname[i] + ".html", "w")
    htmlfile.write(pystache.render(template, datafiles[i]))
    i += 1


if __name__ == "__main__":
  main()
