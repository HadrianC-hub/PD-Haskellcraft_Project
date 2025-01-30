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
# Dibujar el mapa del juego
def draw_map(position, size, player_energy, opponent_energy, player_actions):
    global player_camp_position, opponent_camp_position, WEATHER

    # Obtener las dimensiones actuales de la consola
    terminal_size = shutil.get_terminal_size()
    terminal_width = terminal_size.columns
    terminal_height = terminal_size.lines

    # Calcular márgenes para centrar el mapa
    horizontal_margin = max((terminal_width - (size * 2)) // 2, 0)  # Cada celda ocupa 2 espacios (carácter + espacio)
    vertical_margin = max((terminal_height - size) // 2, 0)

    os.system("cls" if os.name == "nt" else "clear")  # Limpiar consola

    # Dibujar la línea de energía en la parte superior del mapa
    energy_line = f"ENERGÍA DEL JUGADOR: {player_energy}    ENERGÍA DEL OPONENTE: {opponent_energy}"
    hunger_thirst_line = f"HAMBRE: {player_hunger}    SED: {player_thirst}              HAMBRE: {opponent_hunger}    SED: {opponent_thirst}"
    print(energy_line.center(terminal_width))  # Centrar la línea de energía
    print(hunger_thirst_line.center(terminal_width))  # Centrar la línea de hambre y sed

    day_weather = "Desconocido"
    if WEATHER == 0:
        day_weather = "NUBLADO"
    if WEATHER == 1:
        day_weather = "SOLEADO"
    if WEATHER == 2:
        day_weather = "LLUVIOSO"
    if WEATHER == 3:
        day_weather = "NEBLINOSO"    
    if WEATHER == 4:
        day_weather = "FRÍO"    
    print(f"CLIMA: {day_weather}".center(terminal_width)) # Imprimir línea del clima

    # Imprimir líneas vacías para el margen superior
    print("\n" * vertical_margin, end="")

    # Dibujar el mapa centrado
    for y in range(size):
        print(" " * horizontal_margin, end="")  # Margen izquierdo
        for x in range(size):
            if (x, y) == position:
                print("\033[34mO\033[0m", end=" ")  # Personaje en azul
            elif (x, y) == opponent_position:
                print("\033[31mO\033[0m", end=" ")  # Personaje en rojo
            elif (x, y) in resources["wood"]:
                if WEATHER == 3:
                    print("\033[37mX\033[0m", end=" ")
                else:
                    print("\033[92mX\033[0m", end=" ")  # Madera en verde claro
            elif (x, y) in resources["water"]:
                if WEATHER == 3:
                    print("\033[37mX\033[0m", end=" ")
                else:
                    print("\033[96mX\033[0m", end=" ")  # Agua en azul claro
            elif (x, y) in resources["food"]:
                if WEATHER == 3:
                    print("\033[37mX\033[0m", end=" ")
                else:
                    print("\033[91mX\033[0m", end=" ")  # Comida en rojo claro
            elif (x, y) == player_camp_position:
                print("\033[34mA\033[0m", end=" ")
            elif (x, y) == opponent_camp_position:
                print("\033[31mA\033[0m", end=" ")
            else:
                print(".", end=" ")  # Dibujar terreno
        print()  # Nueva línea al final de cada fila
    print("\n")
    print(f"Quedan {player_actions} acciones disponibles para hoy".center(terminal_width))
# Función para mostrar la pantalla de GAME OVER
def show_game_over():
    os.system("cls" if os.name == "nt" else "clear")  # Limpiar consola
    print("\n\n\n")
    print("GAME OVER!")
    print("\n\nPresiona cualquier tecla para salir...")
    with keyboard.Events() as events:
        events.get()  # Espera a que se presione cualquier tecla
