""" A setuptools based setup module.See:https://packaging.python.org/en/latest/distributing.htmlhttps://github.com/pypa/sampleproject"""from __future__ import absolute_import, division, print_function  # unicode_literalsimport osimport sys# To use a consistent encodingfrom codecs import open# Always prefer setuptools over distutilsfrom setuptools import setup, find_packagesfrom setuptools.command.test import test as test_command# ---------------------------------------------------------------------------#                             Some helper stuff# ---------------------------------------------------------------------------if 'bdist_wininst' in sys.argv:    if len(sys.argv) > 2 and ('sdist' in sys.argv or 'bdist_rpm' in sys.argv):        print("Error: bdist_wininst must be run alone. Exiting.")        sys.exit(1)here = os.path.abspath(os.path.dirname(__file__))def is_windows():    """ Check if the current OS is Windows """    return (sys.platform == 'win32') or (os.name is "nt")def txt_read(*paths):    """ Build a file path from *paths* and return the textual contents """    with open(os.path.join(here, *paths), encoding='utf-8') as f:        return f.read()class PyTest(test_command):    """ Testing class """    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]    def initialize_options(self):        test_command.initialize_options(self)        self.pytest_args = None    def finalize_options(self):        test_command.finalize_options(self)        self.test_args = []        self.test_suite = True    def run_tests(self):        # import here, because outside the eggs aren't loaded        import pytest        error_no = pytest.main(self.pytest_args or [] + ["hydroffice/bag/tests"])        sys.exit(error_no)# ---------------------------------------------------------------------------#                      Populate dictionary with settings# ---------------------------------------------------------------------------# Create a dict with the basic information that is passed to setup after keys are added.setup_args = dict()setup_args['name'] = 'hydroffice.bag'setup_args['version'] = '0.2.3.dev1'setup_args['url'] = 'https://bitbucket.org/gmasetti/hyo_bag/'setup_args['license'] = 'BSD-like license'setup_args['author'] = 'Giuseppe Masetti, Brian R. Calder (CCOM/JHC, UNH)'setup_args['author_email'] = 'gmasetti@ccom.unh.edu, brc@ccom.unh.edu'## descriptive stuff#description = 'A package to manage Bathymetric Attributed Grid (BAG) data files.'setup_args['description'] = descriptionif 'bdist_wininst' in sys.argv:    setup_args['long_description'] = descriptionelse:    setup_args['long_description'] = (txt_read('README.rst') + '\n\n\"\"\"\"\"\"\"\n\n' +                                      txt_read('HISTORY.rst') + '\n\n\"\"\"\"\"\"\"\n\n' +                                      txt_read('AUTHORS.rst') + '\n\n\"\"\"\"\"\"\"\n\n' +                                      txt_read('CONTRIBUTING.rst') + '\n\n\"\"\"\"\"\"\"\n\n' +                                      txt_read('BANNER.rst'))setup_args['classifiers'] = \    [  # https://pypi.python.org/pypi?%3Aaction=list_classifiers        'Development Status :: 4 - Beta',        'Intended Audience :: Science/Research',        'Natural Language :: English',        'License :: OSI Approved :: BSD License',        'Operating System :: OS Independent',        'Programming Language :: Python',        'Programming Language :: Python :: 2',        'Programming Language :: Python :: 2.7',        'Programming Language :: Python :: 3',        'Programming Language :: Python :: 3.4',        'Topic :: Scientific/Engineering :: GIS',        'Topic :: Office/Business :: Office Suites',    ]setup_args['keywords'] = "hydrography ocean mapping survey bag"## code stuff## requirementssetup_args['setup_requires'] =\    [        "setuptools",        "wheel",    ]setup_args['install_requires'] =\    [        "h5py",        "lxml",    ]setup_args['tests_require'] =\    [        "pytest",        "pytest-cov",    ]setup_args['cmdclass'] =\    {        "test": PyTest,    }# hydroffice namespace, packages and other filessetup_args['namespace_packages'] = ['hydroffice']setup_args['packages'] = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "*.test*",                                                ])setup_args['package_data'] =\    {        '': ['media/*.png', 'media/*.ico', 'media/*.icns', 'media/*.txt',],        'hydroffice.bag': [            'iso19139/bag/*',            'iso19139/gco/*',            'iso19139/gmd/*',            'iso19139/gmi/*',            'iso19139/gml/*.xsd',            'iso19139/gml/*.txt',            'iso19139/gml/3.1.1/smil/*',            'iso19139/gsr/*',            'iso19139/gss/*',            'iso19139/gts/*',            'iso19139/xlink/*',            'iso19757-3/*',            'samples/*',        ],    }setup_args['options'] = \    {        "bdist_wininst":        {            "bitmap": "hydroffice/bag/gui/media/hydroffice_wininst.bmp",        }    }# ---------------------------------------------------------------------------#                            Do the actual setup now# ---------------------------------------------------------------------------print(" >> %s" % setup_args['packages'])setup(**setup_args)