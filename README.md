# pycanvas
tiny canvas library

WARNING: The code is horrible at the moment, kinda just a proof of concept for linux

The idea here is to have a tiny library that has few dependencies, can work multi-platform and can go from installation to a working visualisation in under a minute.

It should be able to perform the lowest common denominator of 2D drawing functionality, leaving stuff like graphs/charts/other visualisations as a task for the user/other libraries.

## Installation (or rather usage atm)
### Centos
```
sudo yum install cairo-devel python-devel
pip install --user git+https://github.com/pygobject/pycairo.git
git clone https://github.com/crazyhatfish/pycanvas.git
cd pycanvas
python canvas.py
```
### Windows (wip)
note to self: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycairo

## todo
* [ ] Clean up code
* [ ] Proper event support
* [ ] Turn into proper module
* [ ] Windows support
* [ ] Mac support
* [ ] Everything else
