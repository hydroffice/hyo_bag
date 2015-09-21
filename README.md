hyo_bag
===========

The `hyo_bag` package is focused on the BAG data format developed by the Open Navigation Surface.

About HydrOffice
-----------------------

HydrOffice is a research development environment for ocean mapping. Its aim is to provide a collection of hydro-packages to deal with specific issues in such a field, speeding up both algorithms testing and research-2-operation.

About this hydro-package
-----------------------

This package is heavily based on the `h5py` Python library.


Useful Mercurial commands
-----------------------

### Merge a branch to default

* `hg update default`
* `hg merge 1.0.0`
* `hg commit -m"Merged 1.0.2 branch with default" -ugiumas`
* `hg update 1.0.0`
* `hg commit -m"Close 1.0.2 branch" -ugiumas --close-branch`

### Open a new branch

* `hg update default`
* `hg branch 1.0.1`
* `hg commit -m"Created 1.0.3 branch" -ugiumas`
    
Other info
----------

* Bitbucket: https://bitbucket.org/gmasetti/hyo_bag
* Project page: http://ccom.unh.edu/project/hydroffice
* License: BSD-like license (See COPYING)