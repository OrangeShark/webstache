webstache
=========
webstache is a command line program which generates static webpages using mustache templates and markdown pages as input for the templates. Typing into the command line 
```bash
webstache [directory]
```
will output the generated HTML pages from the specified directory or the current working directory if left empty. 

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
├── css
├── js
└── _src
    ├── layouts
    │   ├── indexpost.mustache
    │   ├── page.mustache
    │   ├── post.mustache
    └── posts
        ├── 2013-04-13-bar.md
        ├── 2014-01-24-foo-bar.md
        ├── 2014-12-24-hello-world.md
        ├── 2015-01-05-a-new-post.md
        ├── 2015-02-11-some-scheme.md
        └── 2015-03-15-clojure.md
```

`config.json` is the configuration file.
`_src/layouts` directory contains the layout templates with page.mustache being the main template used for each page.
`_src/posts` directory contains all the blog posts with the name format yyyy-mm-dd-htmlname.md.

The location of the above files and directories can be specified in the config.
