"""A helper module for configuring HDF5"""


def try_from_h5cc():
    """Try locate hdf5 from the h5cc tool"""
    import subprocess as sp
    import sys
    try:
        h5cc = sp.Popen(['h5cc', '-show'], stdout=sp.PIPE)
    except OSError:
        return False, [None, None]
    while h5cc.poll() is None:
        pass
    if h5cc.poll():
        # didn't return success
        return False, [None, None]
    args = h5cc.stdout.readlines()[0]
    if sys.version_info[0] > 2:
        args = args.decode('utf-8')
    args = args.split(' ')
    incs = ''
    libs = ''
    for arg in args:
        if arg.startswith('-I'):
            incs += ':' + arg[2:]
        elif arg.startswith('-L'):
            libs += ':' + arg[2:]
    return True, [incs[1:], libs[1:]]


def try_sys_h5(is_user):
    """Try locate system installed h5, is user is sepcified, then a
    search of USER_BASE will also be performed
    """
    import distutils
    import os
    import tempfile
    from distutils.ccompiler import get_default_compiler, new_compiler

    def safe_remove(filename):
        try:
            os.remove(filename)
        except OSError:
            pass

    test_file_name = tempfile.gettempdir() + os.sep + 'foo.c'
    test_src_code = open(test_file_name, 'w')
    test_src_code.write('#include \"hdf5.h\"\nint main(void){return 0;}')
    test_src_code.close()

    compiler = new_compiler(get_default_compiler())
    incs = []
    libs = []
    if is_user:
        from site import USER_BASE
        incs.append(USER_BASE + os.sep + 'include')
        libs.append(USER_BASE + os.sep + 'lib')
        incs.append(USER_BASE + os.sep + 'hdf5' + os.sep + 'include')
        libs.append(USER_BASE + os.sep + 'hdf5' + os.sep + 'lib')

    h5cfg = [None if not incs else ':'.join(
        incs), None if not libs else ':'.join(libs)]

    try:
        compiler.compile([test_file_name], include_dirs=incs)
        safe_remove(test_file_name)
        return True, h5cfg
    except distutils.errors.CompileError:
        safe_remove(test_file_name)
        return False, h5cfg


def install_from_scratch(is_user, major, minor):
    """Download HDF5 and compile from source, only work on Linux

    By default, install at /usr/local/cgns_wrapper
    If user is True, then install at USER_BASE/cgns_wrapper
    """
    import tarfile
    import wget
    import os
    import sys

    if is_user:
        from site import USER_BASE
        prefix = USER_BASE + '/cgns_wrapper'
    else:
        prefix = sys.prefix + '/cgns_wrapper'
    minor = str(minor)
    h5v = major + '.' + str(minor)
    tarname = 'hdf5-{}.tar.gz'.format(h5v)

    url = 'https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-{}/hdf5-{}/src/{}'.format(
        major, h5v, tarname)

    fname = wget.download(url)

    tar = tarfile.open(tarname, 'r:gz')
    tar.extractall()
    tar.close()

    cwd = os.getcwd()

    os.chdir(cwd + '/hdf5-{}'.format(h5v))
    ret = os.system(
        './configure --prefix={} && make && make install'.format(prefix))
    if ret:
        raise OSError('build HDF5 failed')

    os.chdir(cwd)

    return [prefix + '/include', prefix + '/lib']
