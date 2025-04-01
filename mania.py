if __name__ != "__main__":
    print(f"Do not import this file! ({__name__})")

import pygame
import os
import configparser

# default values
FPS = 60
WINDOW_W = 800
WINDOW_H = 600

FAILED = False

FOLDER_PATH = os.path.dirname(os.path.abspath(__name__))
CONFIG_PATH = os.path.join(FOLDER_PATH, "config.ini")

config_parser = configparser.ConfigParser()
def init_config(path:str):
    if not os.path.exists(path):
        print(f"Config file doesn't exists: '{path}'")
        return FAILED
    if os.path.isdir(path):
        print(f"Config file cannot be a folder! '{path}'")
        return FAILED

    config_parser.read(path)
    if not "window" in config_parser:
        print(f"No window class in the .ini file: '{path}'")
    else:
        FPS = config_parser["window"].getint("fps", fallback=FPS)
        WINDOW_W = config_parser["window"].getint("width", fallback=WINDOW_W)
        WINDOW_H = config_parser["window"].getint("height", fallback=WINDOW_H)
    
    return True

if init_config(CONFIG_PATH) == FAILED:
    exit()
    
pygame.init()

def game_display():
    pass

def game_inputs():
    pass

def game_loop():
    pass

def main_display():
    pass

def main_inputs():
    pass

def main_loop():
    game_loop()

main_loop()
pygame.quit()