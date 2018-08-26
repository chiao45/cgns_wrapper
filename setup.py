import re
import sys
import codecs
from setuptools.command.build_py import build_py
from setuptools import setup
from hdf5_config import try_from_h5cc, try_sys_h5, install_from_scratch
from embed_pycgns import embed_pycgns

HDF5_FALLBACK_MAJOR = '1.10'
HDF5_FALLBACK_MINOR = 3

PYCGNS_URL = 'https://github.com/pyCGNS/pyCGNS/archive/master.zip'

vfile = open('cgns_wrapper/_version.py', mode='r')
vstr_raw = vfile.read()
vstr_find = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", vstr_raw, re.M)
if vstr_find:
    version = vstr_find.group(1)
else:
    raise RuntimeError(
        'Unable to find __version__ in cgns_wrapper/_version.py.')
vfile.close()

install_requires = [
    'numpy',
    'setuptools',
    'wget',
    'Cython>=0.25',
    'future'
]

IS_USER = True if '--user' in sys.argv else False


def found_h5(cfg):
    return cfg[0]


# Try to find h5 from h5cc tool
h5cfg = try_from_h5cc()
if not found_h5(h5cfg):
    h5cfg = try_sys_h5(IS_USER)
    if not found_h5(h5cfg):
        h5cfg = install_from_scratch(
            IS_USER, HDF5_FALLBACK_MAJOR, HDF5_FALLBACK_MINOR)
        h5cfg = [None, h5cfg]
h5cfg = h5cfg[1]


class EmbedPyCGNSBuild(build_py, object):
    def run(self):
        import os
        super(EmbedPyCGNSBuild, self).run()
        build_path = self.build_lib + os.sep + 'cgns_wrapper'
        embed_pycgns(PYCGNS_URL, h5cfg, build_path)


classifiers = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: MIT License',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development',
    'Operating System :: POSIX :: Linux',
    'Intended Audience :: Science/Research',
]

pkgs = ['cgns_wrapper', 'cgns_wrapper.CGNS']

setup(
    name='cgns_wrapper',
    version=version,
    description='Using CGNS in Python',
    long_description=codecs.open('README.rst', encoding='utf-8').read(),
    author='Qiao Chen',
    author_email='benechiao@gmail.com',
    keywords='Math',
    license='MIT',
    url='https://github.com/chiao45/cgns_wrapper',
    packages=pkgs,
    install_requires=install_requires,
    classifiers=classifiers,
    cmdclass={'build_py': EmbedPyCGNSBuild},
    data_files=[('', ['hdf5_config.py', 'embed_pycgns.py'])]
)
