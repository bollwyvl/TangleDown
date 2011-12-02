#!/usr/bin/env python
from setuptools import setup, find_packages
import sys, os

from tangledown.version import __version__

setup(name='TangleDown',
      version=__version__,
      description="Markdown + Tangle.js",
      long_description="""
Use the Markdown syntax to create reactive documents
""",
      classifiers=[], 
      keywords='',
      author='Nicholas Bollweg',
      author_email='nick.bollweg@gmail.com',
      url='https://github.com/bollwyvl/tangledown',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'Markdown==2.1.0',
          'Pinax==0.9a2',
      ]
      )