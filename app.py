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

#           Funciones de dibujado:

# Dibujar menú principal
def draw_main_menu():
    title = """
  _   _           _   _                    _____  _   
 | | | |         | | | |                  |  ___|| |  
 | |_| | __ _ ___| |_| /  ___  ____  __ _ | |_ |_   _|
 |  _  |/ _` / __| '_ \ / ___||  __|/ _` /|  _|  | |  
 | | | | (_| \__ \ | | | |___ | |  | (_|  | |    | |  
 \_| |_/\__,_|___/_| |_|\ ___||_|   \__,_||_|    |_|  
    """
    
    description = """
    Un juego hecho por:
    Adrián Hernández Castellanos C-312
    Laura Martir Beltrán C-311
    Yesenia Valdés Rodríguez C-311
    y Haskell...

    Presione cualquier tecla para jugar !!!
    """

    # Obtener tamaño de la consola
    terminal_size = shutil.get_terminal_size()
    terminal_width = terminal_size.columns

    os.system("cls" if os.name == "nt" else "clear")  # Limpiar consola

    # Calcular margen horizontal para centrar el texto
    title_lines = title.split("\n")
    for line in title_lines:
        print(line.center(terminal_width))

    print("\n")

    description_lines = description.split("\n")
    for line in description_lines:
        print(line.center(terminal_width))
# Función para mostrar la pantalla de GAME OVER
def show_game_over():
    os.system("cls" if os.name == "nt" else "clear")  # Limpiar consola
    print("\n\n\n")
    print("GAME OVER!")
    print("\n\nPresiona cualquier tecla para salir...")
    with keyboard.Events() as events:
        events.get()  # Espera a que se presione cualquier tecla
