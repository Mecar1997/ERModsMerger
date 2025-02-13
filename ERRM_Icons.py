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

def replace_witchyxml(initial_name, new_name, filepath):
    with open(os.path.join(filepath, "_witchy-tpf.xml"), 'r') as file:
        filedata = file.read()
        filedata = filedata.replace(initial_name, new_name)
        with open(os.path.join(filepath, "_witchy-tpf.xml"), 'w') as file:
            file.write(filedata)

def unpack_101_sorceries_icons():
    print("------------ Setting up 101 Sorceries' icons")
    # Copy icons from 101 sorceries' Gideon Folder
    from_directory = ".\\101Sorceries\\menu\\deploy\\projects\\101_sorceries"
    to_directory = ".\\Output\\menu\\deploy\\projects\\ELDENRINGReforged"
    shutil.copytree(from_directory, to_directory)
    # Project.ini
    with open(os.path.join(to_directory, "project.ini"), 'r') as file:
        lines = file.readlines()
    lines[0] = "ELDEN RING Reforged\n"
    with open(os.path.join(to_directory, "project.ini"), 'w') as file:
        file.writelines(lines)
    # Rename MENU_Knowledge files (unpack + repack) + Mapping file
    rename_icon("ge_0", "ge_2", to_directory + "\\solo" )
    with open(os.path.join(to_directory + "\\solo", "mappings.ini"), 'r') as file:
        filedata = file.read()
    filedata = filedata.replace("MENU_Knowledge_0", "MENU_Knowledge_2")
    with open(os.path.join(to_directory + "\\solo", "mappings.ini"), 'w') as file:
        file.write(filedata)
    # Rename Layout file
    path = to_directory + "\\layout"
    os.rename(os.path.join(path, "SB_Icon_02_A.layout"), os.path.join(path, "SB_Icon_02_101.layout"))
    rename_layout_file("SB_Icon_02_101.layout", path, 'ItemIcon_0', 'ItemIcon_2', 'Icon_02_A', 'Icon_02_101')
    # Rename Common files (unpack + repack)
    path = to_directory + "\\common"
    os.rename(os.path.join(path, "SB_Icon_02_A.tpf.dcx"), os.path.join(path, "SB_Icon_02_101.tpf.dcx"))
    subprocess.call('{}\\WitchyBND.exe -u {}\\SB_Icon_02_101.tpf.dcx'.format(WITCHYBND_PATH, path))
    replace_witchyxml('02_A', '02_101', path + "\\SB_Icon_02_101-tpf-dcx")
    os.rename(os.path.join(path + "\\SB_Icon_02_101-tpf-dcx", "SB_Icon_02_A.dds"), os.path.join(path + "\\SB_Icon_02_101-tpf-dcx", "SB_Icon_02_101.dds"))
    repack_witchy('\\SB_Icon_02_101-tpf-dcx', 'SB_Icon_02_101.tpf.dcx', path)
    print("------------ Icons setup done")


def rename_icon(initial_name, new_name, to_directory):
    path = to_directory  
    for f in os.listdir(path):
        if initial_name in f:
            os.rename(os.path.join(path, f), os.path.join(path, f.replace(initial_name, new_name)))    
    for f in os.listdir(path):
        if new_name in f:
            logging.debug("New file name: " + f)
            # unpack & rename the files inside
            unpacked_folder_name = '\\' + f.replace(".", "-")
            subprocess.call('{}\\WitchyBND.exe -u {}'.format(WITCHYBND_PATH, os.path.join(path, f)))
            replace_witchyxml(initial_name, new_name, path + unpacked_folder_name)
            for f2 in os.listdir(path+unpacked_folder_name):
                logging.debug(f2)
                if "MENU_Knowledge" in f2:
                    os.rename(os.path.join(path + unpacked_folder_name, f2), os.path.join(path + unpacked_folder_name, f2.replace(initial_name, new_name)))
            logging.debug(unpacked_folder_name)
            repack_witchy(unpacked_folder_name, f, path)


def rename_layout_file(filename, path, icon_name_old, icon_name_new, title_old, title_new):
    with open(os.path.join(path, filename), 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(icon_name_old, icon_name_new)
    filedata = filedata.replace(title_old, title_new)
    with open(os.path.join(path, filename), 'w') as file:
        file.write(filedata)

def repack_witchy(unpacked_folder, packed_file, path):
    f = os.path.join(path, packed_file)
    if os.path.exists(f):
        os.remove(f)
    subprocess.call('{}\\WitchyBND.exe -r {}'.format(WITCHYBND_PATH, path + unpacked_folder))
    if os.path.exists(path + unpacked_folder):
        shutil.rmtree(path + unpacked_folder)



def unpack_convergence_icons():
    print("------------ Setting up Convergence icons")
    # Copy icons from 101 sorceries' Gideon Folder
    from_directory = ".\\Convergence\\menu\\hi"
    to_directory = ".\\Output\\menu\\hi"
    shutil.copytree(from_directory, to_directory)
    # Unpack everything
    subprocess.call(WITCHYBND_PATH + '\\WitchyBND.exe -u' + to_directory +'\\01_common.tpf.dcx')
    # subprocess.call(WITCHYBND_PATH + '\WitchyBND.exe -u' + to_directory +'\\00_solo.tpfbdt')
    subprocess.call(WITCHYBND_PATH + '\\WitchyBND.exe -u' + to_directory +'\\00_solo.tpfbhd')
    subprocess.call(WITCHYBND_PATH + '\\WitchyBND.exe -u' + to_directory +'\\01_common.sblytbnd.dcx')
    # Create Gideon folder
    to_directory_gideon = ".\\Output\\menu\\deploy\\projects\\ELDENRINGReforged"
    # Rename MENU_Knowledge files (unpack + repack)
    path = to_directory_gideon + "\\solo"
    if not os.path.exists(path):
        os.makedirs(path)
    for f in os.listdir(to_directory + "\\00_solo-tpfbhd"):
       filename = Path(f).stem
       if filename.endswith(".tpf") and filename.startswith("MENU_Knowledge"):
        index = filename.removesuffix(".tpf").removeprefix("MENU_Knowledge_")
        index = int(index)
        if (index >= 3732 and index <= 8202) or (index >= 45000 and index <= 45479):
            shutil.move(os.path.join(to_directory + "\\00_solo-tpfbhd", f), os.path.join(path, f))
    rename_icon("MENU_Knowledge_0", "MENU_Knowledge_5", path)
    rename_icon("MENU_Knowledge_4", "MENU_Knowledge_5", path)
    # Rename Layout file
    path = to_directory_gideon + "\\layout"
    if not os.path.exists(path):
        os.makedirs(path)
    shutil.move(to_directory +'\\01_common-sblytbnd-dcx\\SB_Icon_02_A.layout', path + '\\SB_Icon_02_A_CER.layout')
    rename_layout_file("SB_Icon_02_A_CER.layout", path, 'ItemIcon_0', 'ItemIcon_5', '02_A', '02_A_CER')
    shutil.move(to_directory +'\\01_common-sblytbnd-dcx\\SB_Icon_02_C.layout', path + '\\SB_Icon_02_C_CER.layout')
    rename_layout_file("SB_Icon_02_C_CER.layout", path, 'ItemIcon_4', 'ItemIcon_5', '02_C', '02_C_CER')
    shutil.move(to_directory +'\\01_common-sblytbnd-dcx\\SB_Icon_02_D.layout', path + '\\SB_Icon_02_D_CER.layout')
    rename_layout_file("SB_Icon_02_D_CER.layout", path, 'ItemIcon_4', 'ItemIcon_5', '02_D', '02_D_CER')
    # Rename Common files (unpack + repack)
    path = to_directory_gideon + "\\common"
    names = ['SB_Icon_02_A_CER', 'SB_Icon_02_C_CER', 'SB_Icon_02_D_CER']
    names_old = ['SB_Icon_02_A', 'SB_Icon_02_C', 'SB_Icon_02_D']
    for name, name_old in zip(names, names_old):
        if not os.path.exists('{}\\{}-tpf-dcx'.format(path, name)):
            os.makedirs('{}\\{}-tpf-dcx'.format(path, name))
            shutil.move('{}\\01_common-tpf-dcx\\{}.dds'.format(to_directory, name_old), '{}\\{}-tpf-dcx\\{}.dds'.format(path, name, name))
            shutil.copy("{}menu\\deploy\\projects\\ELDENRINGReforged\\common\\{}-tpf-dcx\\_witchy-tpf.xml".format(overwrite_folder, name), '{}\\{}-tpf-dcx\\_witchy-tpf.xml'.format(path, name))
            repack_witchy('\\{}-tpf-dcx'.format(name), '{}.tpf.dcx'.format(name), path)
    # Delete hi folder
    if os.path.exists(to_directory):
        shutil.rmtree(to_directory)
    print("------------ Icons setup done")


# Unpack 101 sorceries icons, rename everything, repack
unpack_101_sorceries_icons()
unpack_convergence_icons()
# shutil.copy(overwrite_folder + "menu\deploy\projects\\ELDENRINGReforged\project.ini", path + '\SB_Icon_CER-tpf-dcx\_witchy-tpf.xml')