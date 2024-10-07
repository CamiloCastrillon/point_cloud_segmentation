import os
import subprocess
import sys

def whereis(afile):
    """
        return directory in which afile is, None if not found. Look in PATH
    """
    if sys.platform.startswith('win'):
        cmd = "where"
    else:
        cmd = "which"
    try:
        ret = subprocess.run([cmd, afile], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
        return print(os.path.split(ret.stdout.decode())[0])
    except subprocess.CalledProcessError:
        return None

whereis("openMVG_main_SfMInit_ImageListing")