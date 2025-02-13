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

# TODO: redirect print outputs to a log file

def read_files(module_directory):
    for filename in os.listdir(module_directory):
        f = os.path.join(module_directory, filename)
        if filename.endswith("CSV"):
            execute_csv(f)
        elif filename.endswith("massedit"):
            execute_massedit(f)
        elif filename.startswith("sfx_mapping"):
            sfx_mapping(f)
        elif filename.startswith("parts_mapping"):
            parts_mapping(f)
        elif filename.startswith("msgmenu"):
            for msg_filename in os.listdir(f):
                f2 = os.path.join(f, msg_filename)
                execute_fmg_merge(f2, False)
        elif filename.startswith("msgitem"):
            for msg_filename in os.listdir(f):
                f2 = os.path.join(f, msg_filename)
                execute_fmg_merge(f2)
        elif filename.startswith("tae"):
            merge_taes(f)
        elif filename.startswith("behbnd"):
            merge_behbnd(f)
        elif filename.startswith("SubModule_"):
            print("----------------------- Merging submodule: " + f)
            read_files(f)
        #elif filename.startswith("anim_mapping"):
        #    anims_mapping(f)
        # TODO:
        elif filename.startswith("anims"):
            merge_anims(f)
        elif filename.startswith("chr"):
            shutil.copytree(f,  ".\\Output\\chr", dirs_exist_ok=True)
        elif filename.startswith("action"):
            shutil.copytree(f,  ".\\Output\\action", dirs_exist_ok=True)
        elif filename.startswith("event"):
            shutil.copytree(f,  ".\\Output\\event", dirs_exist_ok=True)
        elif filename.startswith("map"):
            shutil.copytree(f,  ".\\Output\\map", dirs_exist_ok=True)
        elif filename.startswith("script"):
            shutil.copytree(f,  ".\\Output\\script", dirs_exist_ok=True)
        elif filename.startswith("sfx"):
            shutil.copytree(f,  ".\\Output\\sfx", dirs_exist_ok=True)
        #TODO: animation mapping / behbnd
        #TODO: map files & event scripts
        #TODO: AI scripts

def execute_module(module_name):
    module_directory = ".\\Modules\\"+ module_name 
    print("----------------------- Merging module: " + module_name)
    read_files(module_directory)

def merge_taes(filepath):
    logging.debug("TAE files found. Merging them")
    subprocess.call('"{}" --animerge ".\\Output\\chr\\c0000.anibnd.dcx" "{}"'.format(DSMSP_PATH, filepath))
    # TODO: Add behbnd merging

def merge_behbnd(filepath):
    if not os.path.exists("{}\\c0000.behbnd.dcx".format(filepath)):
        return
    logging.debug("Behbnd found. Merging.")
    # TODO: Add behbnd merging

def merge_anims(folder):
    logging.debug("anim folder found. Merging.")
    if not os.path.exists(".\\Output\\chr"):
        os.makedirs(".\\Output\\chr")
    for file in os.listdir(folder):
        if not file.endswith(".dcx"):
            continue
        filepath = os.path.join(folder, file)
        if not os.path.exists(".\\Output\\chr\\" + file):
            logging.debug("file does not exist in original mod: " + file)
            shutil.copy(filepath,  ".\\Output\\chr\\" + file)
        else:
            subprocess.call('"{}" --bnddiff "{}" "{}"'.format(DSMSP_PATH, filepath, ".\\Output\\chr\\" + file))
            shutil.move(filepath + ".partial", ".\\Output\\chr\\" + file + ".partial")
            subprocess.call('"{}" --bndmerge "{}" "{}"'.format(DSMSP_PATH, ".\\Output\\chr\\" + file, ".\\Output\\chr\\" + file + ".partial"))
            os.remove(".\\Output\\chr\\" + file + ".partial")


def anims_mapping(filepath):
    with open(filepath, 'r') as file:
        anims = file.read().splitlines() 
    #TODO
    for anim in anims:
        if anim.startswith("-"):
            current_mod = anim.replace("-", "")
            path = ".\\{}\\parts".format(current_mod) #TODO
            continue
        if "|" in anim:
            anim_old, anim_new = anim.split('|', 1)
        else:
            shutil.copy(".\\{}\\{}".format(path, anim),  ".\\Output\\parts\\{}".format(anim)) #TODO


def parts_mapping(filepath):
    if not os.path.exists(".\\Output\\parts"):
        os.makedirs(".\\Output\\parts")
    with open(filepath, 'r') as file:
        parts = file.read().splitlines() 
    for part in parts:
        if part.startswith("-"):
            current_mod = part.replace("-", "")
            path = ".\\{}\\parts".format(current_mod)
            continue
        if "|" in part:
            part_old, part_new = part.split('|', 1)
            shutil.copy(".\\{}\\{}".format(path, part_old),  ".\\Output\\parts\\{}".format(part_new))
        else:
            shutil.copy(".\\{}\\{}".format(path, part),  ".\\Output\\parts\\{}".format(part))
        

#sfx

def sfx_mapping(filepath):
    if not os.path.exists(".\\Output\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd"):
        #os.makedirs(".\\Output\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd\\resource")
        #os.makedirs(".\\Output\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd\\effect")
        #os.makedirs(".\\Output\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd\\texture")
        #os.makedirs(".\\Output\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd\\model")
        #os.makedirs(".\\Output\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd\\animation")
        return
    with open(filepath, 'r') as file:
        sfx_list = file.read().splitlines() 
    for sfx_id in sfx_list:
        if sfx_id.startswith("-"):
            current_mod = sfx_id.replace("-", "")
            path = ".\\{}\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd".format(current_mod)
            continue
        if "|" in sfx_id:
            sfx_id_old, sfx_id_new = sfx_id.split('|', 1)
            fxr_old = "f" + sfx_id_old.zfill(9)
            fxr_new = "f" + sfx_id_new.zfill(9)
            copy_sfx(path, fxr_old, fxr_new)
        else:
            fxr = "f" + sfx_id.zfill(9)
            copy_sfx(path, fxr, fxr)

            
def copy_sfx(path, fxr_old, fxr_new):
    reslist_path = ".\\Output\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd\\resource\\{}.ffxreslist".format(fxr_new)
    if os.path.exists(reslist_path):
        print("WARNING: File {} was overwritten".format(reslist_path))
    shutil.copy(".\\{}\\resource\\{}.ffxreslist".format(path, fxr_old),  reslist_path)
    shutil.copy(".\\{}\\effect\\{}.fxr".format(path, fxr_old),  ".\\Output\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd\\effect\\{}.fxr".format(fxr_new))
    read_ffxreslist(reslist_path, path)

def read_ffxreslist(filepath, old_path):
    with open(filepath, 'r') as file:
        parts = file.read().splitlines() 
    for part in parts:
        if part.endswith(".tif"):
            if os.path.exists(".\\{}\\texture\\{}".format(old_path, part.replace("tif", "dds"))):
                shutil.copy(".\\{}\\texture\\{}".format(old_path, part.replace("tif", "dds")),  ".\\Output\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd\\texture\\{}".format(part.replace("tif", "dds")))
        elif part.endswith(".sib"):
            if os.path.exists(".\\{}\\model\\{}".format(old_path, part.replace("sib", "flver"))):
                shutil.copy(".\\{}\\model\\{}".format(old_path, part.replace("sib", "flver")),  ".\\Output\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd\\model\\{}".format(part.replace("sib", "flver")))
        elif part.endswith("_skeleton.hkt"):
            if os.path.exists(".\\{}\\animation\\{}".format(old_path, part.replace("_skeleton.hkt", ".anibnd"))):
                shutil.copy(".\\{}\\animation\\{}".format(old_path, part.replace("_skeleton.hkt", ".anibnd")),  ".\\Output\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd\\animation\\{}".format(part.replace("_skeleton.hkt", ".anibnd")))
            


def execute_massedit(file):
    logging.debug("Executing massedit file:" + file)
    subprocess.call('"{}" ".\\Output\\regulation.bin" -G ER -P "{}" -M+ "{}"'.format(DSMSP_PATH, GAME_PATH, file))

def execute_fmg_merge(file, item=True):
    if item:
        logging.debug("Merging fmg file to item.msgbnd:" + file)
        subprocess.call('"{}" --fmgmerge ".\\Output\\msg\\engus\\item.msgbnd.dcx" "{}"'.format(DSMSP_PATH, file))
    else:
        logging.debug("Merging fmg file to menu.msgbnd:" + file)
        subprocess.call('"{}" --fmgmerge ".\\Output\\msg\\engus\\menu.msgbnd.dcx" "{}"'.format(DSMSP_PATH, file))

def execute_csv(file):
    logging.debug("Executing csv file:" + file)
    subprocess.call('"{}" ".\\Output\\regulation.bin" -G ER -P "{}" -C "{}"'.format(DSMSP_PATH, GAME_PATH, file))


# Copy regulation.bin, the msg files & c0000 anibd files before we edit them
# TODO: c000.hks
if not os.path.exists(".\\Output\\chr"):
        os.makedirs(".\\Output\\chr")
if not os.path.exists(".\\Output\\sfx"):
        os.makedirs(".\\Output\\sfx")
if not os.path.exists(".\\Output\\action\\script"):
        os.makedirs(".\\Output\\action\\script")
# TODO: if sfx, msg or regulation files from MOD_PATH don't exists, maybe copy from GAME_PATH to avoid errors ?
if os.path.exists(".\\" + MOD_PATH + "\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd"):
    shutil.copytree(".\\" + MOD_PATH + "\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd", ".\\Output\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd")
# TODO: for msg & regulation, implement check if MOD_PATH doesn't have an msg file... in that case copy from GAME_PATH
shutil.copy(".\\action\\script\\c0000.hks",  ".\\Output\\action\\script\\c0000.hks")
shutil.copy(".\\" + MOD_PATH + "\\regulation.bin",  ".\\Output\\regulation.bin")
shutil.copytree(".\\" + MOD_PATH + "\\msg\\engus",  ".\\Output\\msg\\engus")
shutil.copytree(".\\parts",  ".\\Output\\parts")
for file in os.listdir(".\\chr"):
    filepath = os.path.join(".\\chr", file)
    shutil.copy(filepath,  ".\\Output\\chr\\" + file)
for file in os.listdir(".\\" + MOD_PATH + "\\chr"):
    if file.startswith("c000") and file.endswith("anibnd.dcx"):
        filepath = os.path.join(".\\" + MOD_PATH + "\\chr", file)
        shutil.copy(filepath,  ".\\Output\\chr\\" + file)

# Load order
path = ".\\Modules"
with open(".\\loadorder.txt", 'r') as file:
        modules = file.read().splitlines() 
for module in modules:
    execute_module(module)


subprocess.call('{}\\WitchyBND.exe -r ".\\Output\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd"'.format(WITCHYBND_PATH))
# TODO: os.remove(".\\Output\\sfx\\sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd")