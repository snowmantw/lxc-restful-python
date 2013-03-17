
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
3. Enabled global site-packages by command: `toggleglobalsitepackages`
4. After that, the module can be successfully loaded

References

1. [Manual of the virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html)
