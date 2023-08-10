"""A module for using efficient leave-one-out knockoff construction in Python."""

from setuptools import setup, find_packages
import pathlib
import numpy as np

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')
setup(
    name='pylookc', 
    version='2.0.0', 
    description='Efficient construction of leave-one-out knockoffs in Python', 
    long_description=long_description, 
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/ekernf01/pylookc',  # Optional
    author='Eric Kernfeld',  
    author_email='eric.kern13@gmail.com', 
    classifiers=[ 
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='knockoffs, leave-one-out knockoffs, structure learning, gene regulatory network',  # Optional
    package_dir={'': 'src'},  # Optional
    packages=find_packages(where='src'), 
    python_requires='>=3.6, <4',
    install_requires=['numpy'], 
    project_urls={ 
        'Bug Reports': 'https://github.com/ekernf01/pylookc/issues',
        'Source': 'https://github.com/ekernf01/pylookc/',
    },
)
