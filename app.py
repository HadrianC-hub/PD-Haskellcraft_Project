import subprocess
import os
import time
from pynput import keyboard  # Asegúrate de que esta biblioteca esté instalada
import shutil
import random

# Variables globales
MAP_SIZE = 10
MOVE_DELAY = 0.1
WEATHER = 3       # 0=nublado   1=soleado   2=lluvioso   3=neblinoso   4=frio
last_command = "init"
exit_game = False
campament_trigger = False
water_trigger = False
food_trigger = False
wood_trigger = False
position = (0,0)

# Variables iniciales de la partida
INITIAL_ENERGY = 50
INITIAL_HUNGER = 50
INITIAL_THIRST = 30
INITIAL_ACTIONS = 3
INITIAL_X_P1 = 0
INITIAL_Y_P1 = 0
INITIAL_X_P2 = 0
INITIAL_Y_P2 = 0

# Variables globales para los recursos
resources = {"wood": [], "water": [], "food": []}
RESOURCE_COUNT = 3  # Número máximo de cada tipo de recurso en el mapa

# Variables del jugador
player_energy = 100
player_hunger = 5
player_thirst = 3
player_actions = 3
player_camp_position = (0,0)

# Variables del oponente
opponent_energy = 100
opponent_hunger = 5
opponent_thirst = 3
opponent_actions = 3
opponent_camp_position = (MAP_SIZE-1,MAP_SIZE-1)
opponent_position = (0,0)

