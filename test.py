import subprocess
from configparser import ConfigParser
import os
import subprocess
import shutil
from pathlib import Path
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# read config.ini
config_object = ConfigParser()
config_object.read("config.ini")
overwrite_folder = ".\\"
paths_config = config_object["PATHS"]
WITCHYBND_PATH = paths_config["WITCHYBND_PATH"]
DSMSP_PATH = paths_config["DSMSP_PATH"] + '\\DSMSPortable.exe'
GAME_PATH = paths_config["GAME_PATH"]
MOD_PATH= paths_config["MOD_PATH"]




filepath = ".\\Modules\\Storm Sorceries\\anims\\c0000_a9x.anibnd.dcx"
file = "c0000_a9x.anibnd.dcx"
subprocess.call('"{}" --bnddiff "{}" "{}"'.format(DSMSP_PATH, filepath, ".\\Output\\chr\\" + file))
shutil.move(filepath + ".partial", ".\\Output\\chr\\" + file + ".partial")
subprocess.call('"{}" --bndmerge "{}" "{}"'.format(DSMSP_PATH, ".\\Output\\chr\\" + file, ".\\Output\\chr\\" + file + ".partial"))
os.remove(".\\Output\\chr\\" + file + ".partial")