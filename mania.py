if __name__ != "__main__":
    print(f"Do not import this file! ({__name__})")

import pygame
import os
import configparser


FPS = 60
WINDOW_W = 800
WINDOW_H = 600
IS_FULLSCREEN = False

TEXTURE_PACK = "Default"

FAILED = False

FOLDER_PATH = os.path.dirname(os.path.abspath(__name__))
MAIN_CONFIG_PATH = os.path.join(FOLDER_PATH, "config.ini")


config_parser = configparser.ConfigParser()
def init_main_config(path:str):
    if not os.path.exists(path):
        print(f"Config file doesn't exists: '{path}'")
        return FAILED
    if os.path.isdir(path):
        print(f"Config file cannot be a folder! '{path}'")
        return FAILED

    config_parser.read(path)
    if not "Window" in config_parser:
        print(f"No Window class in the .ini file: '{path}'")
    else:
        global FPS, WINDOW_W, WINDOW_H, IS_FULLSCREEN
        FPS = config_parser["Window"].getint("fps", fallback=FPS)
        WINDOW_W = config_parser["Window"].getint("width", fallback=WINDOW_W)
        WINDOW_H = config_parser["Window"].getint("height", fallback=WINDOW_H)
        IS_FULLSCREEN = config_parser["Window"].getboolean("fullscreen", fallback=IS_FULLSCREEN)
    
    if not "User" in config_parser:
        print(f"No User class in the .ini file: '{path}'")
    else:
        global TEXTURE_PACK
        TEXTURE_PACK = config_parser["User"].get("Skin", fallback=TEXTURE_PACK)
    
    return True

SKIN_PLACEMENTS = dict()

def set_default_placements():
    SKIN_PLACEMENTS["4K_start_pos_x"] = 400
    SKIN_PLACEMENTS["4K_start_pos_y"] = 0
    SKIN_PLACEMENTS["4K_end_pos_y"] = 700
    SKIN_PLACEMENTS["4K_note_width"] = 100
    SKIN_PLACEMENTS["4K_note_height"] = 70
    SKIN_PLACEMENTS["4K_note_space"] = 50

set_default_placements()

def offset_skin_placements():
    global SKIN_PLACEMENTS

    x_multiply_by = WINDOW_W / 1000
    y_multiply_by = WINDOW_H / 1000

    for key in SKIN_PLACEMENTS:
        if SKIN_PLACEMENTS[key] < 0 or SKIN_PLACEMENTS[key] > 1000:
            print(f"The '{key}' at the current skin config is out of range (0, 1000): '{SKIN_PLACEMENTS[key]}")
            return FAILED
        
        key_last_word = key.split("_")[-1]
        if key_last_word == "width" or key_last_word == "x":
            SKIN_PLACEMENTS[key] = SKIN_PLACEMENTS[key] * x_multiply_by
        elif key_last_word == "height" or key_last_word == "y":
            SKIN_PLACEMENTS[key] = SKIN_PLACEMENTS[key] * y_multiply_by
        else:
            print(f"The key ({key}): doesn't follow a rule (last seperated word must be width, height or x, y)!")

def init_skin_config(path:str):
    if not os.path.exists(path):
        print(f"Skin config file doesn't exists: '{path}'")
        return FAILED
    if os.path.isdir(path):
        print(f"Skin config file cannot be a folder! '{path}'")
        return FAILED
    
    config_parser.read(path)
    if not "Placement" in config_parser:
        print("No Placement class in the skin config!")
    else:
        global SKIN_PLACEMENTS
        SKIN_PLACEMENTS["4K_start_pos_x"] = config_parser["Placement"].getint("4K_start_pos_x",
                                                                              fallback=SKIN_PLACEMENTS["4K_start_pos_x"])
        SKIN_PLACEMENTS["4K_start_pos_y"] = config_parser["Placement"].getint("4K_start_pos_y",
                                                                              fallback=SKIN_PLACEMENTS["4K_start_pos_y"])
        SKIN_PLACEMENTS["4K_end_pos_y"] = config_parser["Placement"].getint("4K_end_pos_y",
                                                                              fallback=SKIN_PLACEMENTS["4K_end_pos_y"])
        SKIN_PLACEMENTS["4K_note_width"] = config_parser["Placement"].getint("4K_note_width",
                                                                              fallback=SKIN_PLACEMENTS["4K_note_width"])
        SKIN_PLACEMENTS["4K_note_height"] = config_parser["Placement"].getint("4K_note_height",
                                                                              fallback=SKIN_PLACEMENTS["4K_note_height"])
        SKIN_PLACEMENTS["4K_note_space"] = config_parser["Placement"].getint("4K_note_space",
                                                                              fallback=SKIN_PLACEMENTS["4K_note_space"])

    return offset_skin_placements()
        
if init_main_config(MAIN_CONFIG_PATH) == FAILED:
    exit()
    
pygame.init()
py_clock = pygame.time.Clock()


class Gameplay:
    def __init__(self):
        self.is_failed = False
        self.textures = dict()
        if not self.load_textures():
            self.is_failed = True
            return
        
        self.rectangles = dict()

    def load_textures(self):
        global TEXTURE_PACK
        textures_path = os.path.join(FOLDER_PATH, "Textures", TEXTURE_PACK)
        if not os.path.exists(textures_path):
            print(f"Texture pack folder: {textures_path}', doesn't exists!")
            TEXTURE_PACK = "Default"
            if not os.path.exists(os.path.join(FOLDER_PATH, "Textures", TEXTURE_PACK)):
                print(f"Default texture pack folder doesn't exists!")
                return FAILED
        
        textures_list = ("Note1", "Note2", "Note3", "Note4")
        for texture in textures_list:
            texture_path = os.path.join(textures_path, f"{texture}.png")
            if not os.path.exists(texture_path):
                texture_path = os.path.join(FOLDER_PATH, "Textures", "Default", texture)
                if not os.path.exists(texture_path):
                    print(f"Must have texture: '{texture_path}, doesn't exists!'")
                    return FAILED
            
            self.textures[texture] = pygame.image.load(texture_path)

        return True
    
    def display(self):
        pass

    def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
        return True

    def loop(self):
        while self.inputs():
            self.display()
            # TODO update notes
            py_clock.tick(FPS)

        # main.loop()


class Main:
    def __init__(self):
        self.is_failed = False
        if not self.load_textures():
            self.is_failed = True
            return
        
        if not init_skin_config(os.path.join(FOLDER_PATH, "Textures", TEXTURE_PACK, "config.ini")):
            self.is_failed = True
            return
        
        self.window = pygame.display.set_mode((WINDOW_W, WINDOW_H), IS_FULLSCREEN)

    def load_textures(self):
        return True # just copy and paste the other one

    def display(self):
        pass

    def inputs(self):
        pass

    def loop(self):
        game.loop()


main = Main()
if main.is_failed:
    pygame.quit()
    exit()    
game = Gameplay()
main.loop()
if game.is_failed:
    pygame.quit()
    exit()
pygame.quit()