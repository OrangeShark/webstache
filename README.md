webstache
=========
webstache is a command line program which generates static webpages using mustache templates and json data files as input. Typing into the command line 
```bash
webstache directory/to/input/files
```
will create a directory called output with the generated HTML pages.

For any file which does not need to be generated, like JavaScript and Cascading Style Sheets, can be put into a directory named static in the input directory. They will be copied over into the root of the output directory.

Read the help for more options
```bash
webstache --help
```

This program is used as an example project for the FIU's Panther Linux User Group's Python workshop.

Installing
----------

### Install with setup.py
Clone the repo to your machine and enter in
```bash
python setup.py install
```
