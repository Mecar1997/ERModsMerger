@echo off




:: DSMSP_PATH is the path to your DSMSPortable executable.
:: MOD_PATH is the path to the folder of the mod you want to merge.
:: GAME_PATH is the path to your ER Game folder
set DSMSP_PATH=D:\Modding\Elden Ring\DSMSPortable
set MOD_PATH=D:\Modding\Elden Ring\ERR
set GAME_PATH="D:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game"


:: DO NOT TOUCH ANYTHING BELOW THIS
set OUTPUT_PATH = .\Output

:: clean temporary files
if exist .\Output\chr\c0000.anibnd.dcx.prev del /q .\Output\chr\c0000.anibnd.dcx.prev
if exist .\Output\chr\c0000_a9x.anibnd.dcx.prev del /q .\Output\chr\c0000_a9x.anibnd.dcx.prev
if exist .\Output\chr\c0000_a9x_rework.anibnd.dcx del /q .\Output\chr\c0000_a9x_rework.anibnd.dcx
if exist .\Output\chr\c0000_a9x_rework.anibnd.dcx.partial del /q .\Output\chr\c0000_a9x_rework.anibnd.dcx.partial
if exist .\Output\chr\c0000_a9x_rework.anibnd.dcx.partial.prev del /q .\Output\chr\c0000_a9x_rework.anibnd.dcx.partial.prev




