webstache
=========
webstache is a command line program which generates static webpages using mustache templates and markdown pages as input for the templates. Typing into the command line 
```bash
webstache [directory]
```
will create a directory called out with the generated HTML pages generated from the specified directory or the current working directory if left empty.

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
# assuming python is python3
sudo python setup.py install
```

Usage
-----

webstache generates webpages based on the contents of the directory. A standard directory looks like this.
```
.
├── config.json
├── layouts
│   └── base.html.mustache
├── pages
│   └── index.md
└── static
    ├── css
    └── js

```

`config.json` is the configuration file.
`layouts` directory contains the layout templates with base.html.mustache being the main template.
`pages` is a directory of markdown pages which will be inserted into the mainContent of each template.
`static` is a directory of files which will be copied over to the output directory.
