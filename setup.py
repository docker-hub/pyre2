#!/usr/bin/env python

import os
import subprocess

from distutils.core import setup, Extension


ROOT_DIR = os.path.dirname(__file__)
C_RE2_PREFIX_DIR = os.path.join(ROOT_DIR, 'build', 'local')
C_RE2_STATIC_LIB = os.path.join(C_RE2_PREFIX_DIR, 'lib', 'libre2.a')
C_RE2_SOURCE_DIR = os.path.join(ROOT_DIR, 're2-master')


def build_c_re2():
    """Build the google/re2 library"""
    os.makedirs(C_RE2_PREFIX_DIR)
    if not os.path.exists(os.path.join(C_RE2_SOURCE_DIR, 'Makefile')):
        subprocess.check_call(['tar', 'zxf', os.path.join(ROOT_DIR, 'c_re2.tar.gz'), '-C', ROOT_DIR])
    subprocess.check_call(['make', '-C', C_RE2_SOURCE_DIR, 'install'], env={"PREFIX": C_RE2_PREFIX_DIR})

if not os.path.exists(C_RE2_STATIC_LIB):
    build_c_re2()


setup(
    name="docker-re2",
    version="1.0.4",
    url="https://github.com/facebook/pyre2",
    description="Python wrapper for Google's RE2",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
    ],
    author="David Reiss",
    author_email="dreiss@fb.com",
    maintainer="Siddharth Agarwal",
    maintainer_email="sid0@fb.com",
    py_modules=["re2"],
    ext_modules=[Extension(
        # We want `libre2.a` to be included into our extension shared library.
        # Do not do any linking against `re2`. Simply list the `.a` file as
        # an input object to link step.
        "_re2",
        sources=["_re2.cc"],
        include_dirs=[os.path.join(C_RE2_PREFIX_DIR, 'include')],
        extra_link_args=[C_RE2_STATIC_LIB]
    )],
)
