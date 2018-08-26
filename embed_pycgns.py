"""Helper module to embed pyCGNS::{MAP,PAT}"""


def embed_pycgns(url, h5cfg, build_path):
    """h5cfg is a list of two arguments:

    first one is include paths with ':' separator
    second one is library paths with ':' separator
    """
    import zipfile
    import wget
    import sys
    import os

    incs = '' if h5cfg[0] is None else '--includes={}'.format(h5cfg[0])
    libs = '' if h5cfg[1] is None else '--libraries={}'.format(h5cfg[1])
    pycgns = zipfile.ZipFile(wget.download(url), 'r')
    pycgns.extractall()
    pycgns.close()

    cwd = os.getcwd()
    os.chdir(cwd + os.sep + 'pyCGNS-master')
    # insert a build_ext into setup.cfg to enable runtime path
    # linking against hdf5, so that non standarded hdf5 installation
    # can be resolved
    if libs != '':
        if sys.version_info[0] < 3:
            import ConfigParser as cp
        else:
            import configparser as cp

        setup_cfg = cp.ConfigParser()
        setup_cfg.add_section('build_ext')
        setup_cfg.set('build_ext', 'rpath', h5cfg[1])
        f = open('setup.cfg', 'w')
        setup_cfg.write(f)
        f.close()
    # NOTE that we are in child dir, so use ../
    extra = ['--app 0', '--val 0', '--dat 0',
             '--nav 0', '--build-platlib=../{}'.format(build_path)]
    cmds = [sys.executable, 'setup.py', 'build',
            '{}'.format(incs), '{}'.format(libs)]
    ret = os.system(' '.join(cmds + extra))
    if ret:
        raise OSError('failed building pyCGNS')
    os.chdir(cwd)
