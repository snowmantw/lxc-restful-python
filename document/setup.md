
## Install Requirements

### System Packages

    apt-get install libxml2-dev python-libvirt virtualenv virtuanenvwrapper

### Pip Packages

    pip -r install ./requirements.txt

## Virtualenv and System packages

For instance, if we need to link the `python-libvirt` package in our virtualenv,
we can done this by:

1. Install `virtualenvwrapper` to get more vrtualenv commands
2. Install `python-libvirt` in system path
3. Install `apt-file` and do `apt-file update` to find what paths the package used
3. Use `add2virtualenv` to add those path, include the `.py` module interface file and it's backend `.so` files
   In this case, `.py` files is in the `/usr/share/pyshared` and `.so` files are in the `/usr/lib/pyshared/python2.7`
4. After that, the module can be successfully loaded

Troubles shooting:

1. If paths can only indicate the `.py` module interfnace, but not the `.so` file, Python will complain that can't find it
2. If wrong paths got added, manually remove it at the `_virtualenv_path_extensions.pth` after `cdsitepackages`


References

1. [Manual of the virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html)
