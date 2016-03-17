Linux Mint
==========

This document descibes a tested configuration.

For use with a VM image:

* Download from here: http://www.osboxes.org/linux-mint/#linuxmint-173-rosa-vmware
* Change Display resolution **optional**
* Install VM Tools using Software Manager (select open-vm-tools-desktop) **optional**


Installation:

* Download 64-bit Python 2.7 miniconda: http://conda.pydata.org/miniconda.html 
* Install it from terminal: ``bash Miniconda-latest-Linux-x86_64.sh``
* Install dependencies using conda (since with pip they may fail): ``conda install numpy matplotlib gdal lxml spyder``
* Finally use pip for hydroffice.bag: ``pip install hydroffice.bag``


Test:

* Open Spyder using the terminal: ``spyder``
* Write 
