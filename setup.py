""" A setuptools based setup module.See:https://packaging.python.org/en/latest/distributing.htmlhttps://github.com/pypa/sampleproject"""from __future__ import absolute_import, division, print_function  # unicode_literalsimport osimport sys# To use a consistent encodingfrom codecs import open# Always prefer setuptools over distutilsfrom setuptools import setup, find_packages# ---------------------------------------------------------------------------#                             Some helper stuff# ---------------------------------------------------------------------------if 'bdist_wininst' in sys.argv:    if len(sys.argv) > 2 and ('sdist' in sys.argv or 'bdist_rpm' in sys.argv):        print("Error: bdist_wininst must be run alone. Exiting.")        sys.exit(1)here = os.path.abspath(os.path.dirname(__file__))def is_windows():    """ Check if the current OS is Windows """    return (sys.platform == 'win32') or (os.name is "nt")def txt_read(*paths):    """ Build a file path from *paths* and return the textual contents """    with open(os.path.join(here, *paths), encoding='utf-8') as f:        return f.read()# ---------------------------------------------------------------------------#                      Populate dictionary with settings# ---------------------------------------------------------------------------# Create a dict with the basic information that is passed to setup after keys are added.setup_args = dict()setup_args['name'] = 'hydroffice.bag'setup_args['version'] = '0.2.7'setup_args['url'] = 'https://bitbucket.org/gmasetti/hyo_bag/'setup_args['license'] = 'BSD license'setup_args['author'] = 'Giuseppe Masetti, Brian R. Calder'setup_args['author_email'] = 'gmasetti@ccom.unh.edu, brc@ccom.unh.edu'## descriptive stuff#description = 'A package to manage Bathymetric Attributed Grid (BAG) data files.'setup_args['description'] = descriptionif 'bdist_wininst' in sys.argv:    setup_args['long_description'] = descriptionelse:    setup_args['long_description'] = (txt_read('README.rst') + '\n\n\"\"\"\"\"\"\"\n\n' +                                      txt_read('HISTORY.rst') + '\n\n\"\"\"\"\"\"\"\n\n' +                                      txt_read('AUTHORS.rst') + '\n\n\"\"\"\"\"\"\"\n\n' +                                      txt_read(os.path.join('docs', 'how_to_contribute.rst')) +                                      '\n\n\"\"\"\"\"\"\"\n\n' + txt_read(os.path.join('docs', 'banner.rst')))setup_args['classifiers'] = \    [  # https://pypi.python.org/pypi?%3Aaction=list_classifiers        'Development Status :: 4 - Beta',        'Intended Audience :: Science/Research',        'Natural Language :: English',        'License :: OSI Approved :: BSD License',        'Operating System :: OS Independent',        'Programming Language :: Python',        'Programming Language :: Python :: 2',        'Programming Language :: Python :: 2.7',        'Programming Language :: Python :: 3',        'Programming Language :: Python :: 3.4',        'Programming Language :: Python :: 3.5',        'Topic :: Scientific/Engineering :: GIS',        'Topic :: Office/Business :: Office Suites',    ]setup_args['keywords'] = "hydrography ocean mapping survey bag openns"## code stuff## requirementssetup_args['setup_requires'] =\    [        "setuptools",        "wheel",    ]setup_args['install_requires'] =\    [        "h5py",        "lxml",    ]# hydroffice namespace, packages and other filessetup_args['namespace_packages'] = ['hydroffice']setup_args['packages'] = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "*.test*",                                                ])setup_args['package_data'] =\    {        '': ['media/*.png', 'media/*.ico', 'media/*.icns', 'media/*.txt',],        'hydroffice.bag': [            'iso19139/bag/*',            'iso19139/gco/*',            'iso19139/gmd/*',            'iso19139/gmi/*',            'iso19139/gml/*.xsd',            'iso19139/gml/*.txt',            'iso19139/gml/3.1.1/smil/*',            'iso19139/gsr/*',            'iso19139/gss/*',            'iso19139/gts/*',            'iso19139/xlink/*',            'iso19757-3/*',            'samples/*',        ],    }setup_args['test_suite'] = "tests"setup_args['entry_points'] =\    {        'console_scripts': ['bag_bbox = hydroffice.bag.tools.bag_bbox:main',                            'bag_elevation = hydroffice.bag.tools.bag_elevation:main',                            'bag_metadata = hydroffice.bag.tools.bag_metadata:main',                            'bag_tracklist = hydroffice.bag.tools.bag_tracklist:main',                            'bag_uncertainty = hydroffice.bag.tools.bag_uncertainty:main',                            'bag_validate = hydroffice.bag.tools.bag_validate:main'],    }setup_args['options'] = \    {        "bdist_wininst":        {            "bitmap": "hydroffice/bag/gui/media/hydroffice_wininst.bmp",        }    }# ---------------------------------------------------------------------------#                            Do the actual setup now# ---------------------------------------------------------------------------print(" >> %s" % setup_args['packages'])setup(**setup_args)