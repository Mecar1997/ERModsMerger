import subprocess
from configparser import ConfigParser
import os
import subprocess
import shutil
from pathlib import Path
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

# read config.ini
config_object = ConfigParser()
config_object.read("config.ini")
overwrite_folder = ".\\"
paths_config = config_object["PATHS"]
WITCHYBND_PATH = paths_config["WITCHYBND_PATH"]
DSMSP_PATH = paths_config["DSMSP_PATH"] + '\\DSMSPortable.exe'
GAME_PATH = paths_config["GAME_PATH"]
MOD_PATH= paths_config["MOD_PATH"]




# Unpack 101 sorceries icons, rename everything, repack


def unpack_mod(mod):
    files_to_unpack = ['sfx\\sfxbnd_commoneffects.ffxbnd.dcx',
                       'script\\aicommon.luabnd.dcx',
                       'chr\\c0000_a5x.anibnd.dcx',
                       'chr\\c0000_a7x.anibnd.dcx',
                       'chr\\c0000_a9x.anibnd.dcx',
                       ]
    for file_to_unpack in files_to_unpack:
        if os.path.exists(".\\{}\\{}".format(mod, file_to_unpack)):
            subprocess.call('"{}\\WitchyBND.exe" -u ".\\{}\\{}"'.format(WITCHYBND_PATH, mod, file_to_unpack))   


if os.path.exists(".\\Convergence"):
    unpack_mod("Convergence")
if os.path.exists(".\\101Sorceries"):
    unpack_mod("101Sorceries")
if os.path.exists(".\\ERR"):
    unpack_mod("ERR")