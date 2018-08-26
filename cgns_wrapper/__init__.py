import os
import sys
from ._version import __version__

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import cgns_wrapper.CGNS.MAP as io
import cgns_wrapper.CGNS.PAT.cgnslib as cgnslib

setattr(cgnslib, 'errors', cgnslib.CE)
setattr(cgnslib, 'keywords', cgnslib.CK)
setattr(cgnslib, 'utils', cgnslib.CU)


def run_tests():
    from .CGNS.PAT.test import run as pat_run
    from .CGNS.MAP.test import run as map_run
    pat_run()
    map_run()
