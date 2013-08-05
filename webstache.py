#!/usr/bin/python

import os, sys, getopt, argparse

def main():
  parser = argparse.ArgumentParser(description='Generates static webpages based off of mustache templates')
  parser.add_argument('directory', nargs='?', default=os.getcwd(), help='Directory of mustache files and data')
  args = parser.parse_args()

  print(args.directory)


if __name__ == "__main__":
  main()
