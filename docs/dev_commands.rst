Development cheatsheet
======================


Useful Mercurial commands
-------------------------

Merge a branch to default
~~~~~~~~~~~~~~~~~~~~~~~~~

* :code:`hg update default`
* :code:`hg merge 2.0.0`
* :code:`hg commit -m"Merged 2.0.0 branch with default" -ugiumas`
* :code:`hg update 2.0.0`
* :code:`hg commit -m"Close 2.0.0 branch" -ugiumas --close-branch`

Open a new branch
~~~~~~~~~~~~~~~~~

* :code:`hg update default`
* :code:`hg branch 2.0.1`
* :code:`hg commit -m"Created 2.0.1 branch" -ugiumas`


Useful git commands
-------------------

Syncing a fork
~~~~~~~~~~~~~~

Add a remote that points to the upstream repo (from the forked project folder):

* :code:`git remote -v` (check before and after if the remote is present)
* :code:`git remote add upstream https://github.com/HDFGroup/hdf-compass`

Fetching from the remote repository:

* :code:`git branch -va` (check all the available branches)
* :code:`git fetch upstream`

Merging with the upstream repository:

* :code:`git checkout master` (to switch to :code:`master` branch)
* :code:`git merge upstream/master`

Finally:

* :code:`git push origin master`

Reset the fork
~~~~~~~~~~~~~~

* :code:`git remote add upstream https://github.com/HDFGroup/hdf-compass`
* :code:`git fetch upstream`
* :code:`git branch backup`
* :code:`git checkout upstream/master -B master`
* :code:`git push --force`

In case of need to retrieve the original code status:

* :code:`git checkout backup`


Documentation
-------------

The documentation is built using `Sphinx`:

* :code:`pip install sphinx sphinx-autobuild`

For the first time, the documentation template is created in the 'docs' folder:

* :code:`mkdir docs`
* :code:`cd docs`
* :code:`sphinx-quickstart`

To update the API documentation:

* :code:`sphinx-apidoc -f -o docs/api hydroffice hydroffice/bag/scripts`

PyPi
----

Some instructions can be found `here <https://wiki.python.org/moin/TestPyPI>`_:

* :code:`python setup.py register -r test`
* :code:`python setup.py register -r pypi`
* :code:`python setup.py build bdist_wheel upload -r test`
* :code:`python setup.py build bdist_wheel upload -r pypi`

Github mirror
-------------

You need to have `hggit <http://hg-git.github.io/>`_ installed.

On Windows, `TortoiseHg <http://tortoisehg.bitbucket.org/>`_ comes with it, but must be enabled in `.hgrc`:

:code:`[extensions]`
:code:`hgext.bookmarks =`
:code:`hggit =`

If not already present, make a bookmark of master for default, so a ref gets created:

:code:`hg bookmark -r default master`
:code:`hg bookmark -f -r 0.2.3 0.2.3`

Add a line like this to the project `.hg/hgrc` under ``[paths]``

:code:`git = git+https://github.com/giumas/hyo_bag.git`

If you don't already have, set up an SSH identity: https://confluence.atlassian.com/bitbucket/set-up-ssh-for-mercurial-728138122.html

