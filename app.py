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

#           Manejo de estado de recursos del juego

# Función para generar recursos aleatoriamente
def generate_resources(size, count):
    """Genera posiciones aleatorias para los recursos en el mapa."""
    positions = set()  # Usamos un conjunto para evitar duplicados
    while len(positions) < count * 3:  # Total de recursos a generar
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        # Verificando que las posiciones generadas no sean de los campamentos ya colocados
        while (x,y) == player_camp_position or (x,y) == opponent_camp_position:
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
        positions.add((x, y))
    
    positions = list(positions)
    resources["wood"] = positions[:count]
    resources["water"] = positions[count:2*count]
    resources["food"] = positions[2*count:]
# Funcion para regenerar recursos
def regenerate_resources(resources, count, map_size, player_camp, opponent_camp):
    # Separando en arrays los valores de recursos
    wood = resources["wood"]
    water = resources["water"]
    food = resources["food"]
    camps = [player_camp, opponent_camp]

    # Determinar cuántos recursos se necesitan
    total_to_generate = count
    generated = 0

    # Crear un conjunto con todas las posiciones ocupadas
    occupied_positions = set(wood + water + food + camps)

    # Listar los recursos que aún pueden recibir elementos
    available_resources = []
    if len(wood) < count:
        available_resources.append("wood")
    if len(water) < count:
        available_resources.append("water")
    if len(food) < count:
        available_resources.append("food")

    # Generar nuevas posiciones de recursos hasta completar `count`
    while generated < total_to_generate and available_resources:
        # Seleccionar un recurso aleatorio de los que aún pueden recibir más elementos
        resource_type = random.choice(available_resources)

        # Generar una posición aleatoria que no esté ocupada
        while True:
            new_x = random.randint(0, map_size - 1)
            new_y = random.randint(0, map_size - 1)
            new_pos = (new_x, new_y)
            if new_pos not in occupied_positions:
                break

        # Insertar la nueva posición en el recurso correspondiente
        if resource_type == "wood":
            wood.append(new_pos)
        elif resource_type == "water":
            water.append(new_pos)
        elif resource_type == "food":
            food.append(new_pos)

        # Agregar la nueva posición a las ocupadas
        occupied_positions.add(new_pos)
        generated += 1

        # Si un recurso llega al máximo, eliminarlo de la lista de disponibles
        if len(wood) >= count and "wood" in available_resources:
            available_resources.remove("wood")
        if len(water) >= count and "water" in available_resources:
            available_resources.remove("water")
        if len(food) >= count and "food" in available_resources:
            available_resources.remove("food")
    
    # Unificando en un array los valores devueltos
    resources = {"wood": wood, "water": water, "food": food}
    return resources
# Funcion para obtener el tipo de recurso en una posición
def get_resource_type_at_position(position, resources):
    global player_camp_position
    if position == player_camp_position:
        return "camp"
    for resource_type, positions in resources.items():
        if position in positions:
            return resource_type  # Devuelve el tipo de recurso encontrado
    return None  # No se encontró ningún recurso en la posición
# Funcion para obtener el estado de recursos
def get_triggers_status():
    global campament_trigger, water_trigger, food_trigger, wood_trigger
    obtained_res = get_resource_type_at_position(position, resources)
    if obtained_res == "wood":
        wood_trigger = True
    if obtained_res == "water":
        water_trigger = True
    if obtained_res == "food":
        food_trigger = True
    if obtained_res == "camp":
        campament_trigger = True
# Función para reiniciar el estado de recursos
def restart_triggers():
    global campament_trigger, water_trigger, food_trigger, wood_trigger
    if campament_trigger:
        campament_trigger = False
    if wood_trigger:
        wood_trigger = False
    if water_trigger:
        water_trigger = False
    if food_trigger:
        food_trigger = False
# Función para generar posición de campamentos aleatoriamente
def set_camps(size):
    global player_camp_position, opponent_camp_position
    camps = set()  # Usamos un conjunto para evitar duplicados
    while len(camps) < 2:  # Total de campamentos a generar
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        camps.add((x, y))
    
    camps = list(camps)
    player_camp_position = camps[0]
    opponent_camp_position = camps[1]
# Función para cambiar el clima
def change_weather():
    global WEATHER
    WEATHER = random.randint(0, 4)



# Función para determinar la tecla presionada y la acción a ejecutar
def on_press(key):
    global last_command, exit_game, show_description, water_trigger, food_trigger, wood_trigger, campament_trigger, resources, position
    try:
        if key == keyboard.Key.up:
            last_command = "up"
        elif key == keyboard.Key.down:
            last_command = "down"
        elif key == keyboard.Key.left:
            last_command = "left"
        elif key == keyboard.Key.right:
            last_command = "right"
        elif hasattr(key, 'char') and key.char == 'q':  # Salir del juego
            exit_game = True
        elif hasattr(key, 'char') and key.char in ('x', 'X'):  # Detección de "X" en minúscula o mayúscula
            if campament_trigger:
                last_command = "end_turn"
                campament_trigger = False
            if water_trigger == True and player_actions > 0:
                last_command = "drink_water"
                water_trigger = False
                resources["water"].remove(position)
            if food_trigger == True and player_actions > 0:
                last_command = "eat_food"
                food_trigger = False
                resources["food"].remove(position)
            if wood_trigger == True and player_actions > 0:
                last_command = "use_wood"
                wood_trigger = False
                resources["wood"].remove(position)
    except AttributeError:
        pass



#           Inicio del juego:

# Inicializando bibliotecas:
listener = keyboard.Listener(on_press=on_press)
listener.start()

try:
    # INICIO DEL MENÚ PRINCIPAL
    draw_main_menu()
    # Espera a que se presione cualquier tecla
    with keyboard.Events() as events:
        events.get()  

    # INICIALIZACIÓN DE LA PARTIDA
    set_camps(MAP_SIZE)
    generate_resources(MAP_SIZE, RESOURCE_COUNT)
    position = player_camp_position
    opponent_position = opponent_camp_position
    INITIAL_X_P1 = player_camp_position[0]
    INITIAL_Y_P1 = player_camp_position[1]
    INITIAL_X_P2 = opponent_camp_position[0]
    INITIAL_Y_P2 = opponent_camp_position[1]
    change_weather()

    # Ejecutar estado inicial de Haskell
    haskell_process = subprocess.Popen(
        ["runhaskell", "game.hs", str(MAP_SIZE), str(INITIAL_ENERGY), str(INITIAL_HUNGER), str(INITIAL_THIRST), str(INITIAL_ACTIONS), str(INITIAL_X_P1), str(INITIAL_Y_P1), str(INITIAL_X_P2), str(INITIAL_Y_P2), str(WEATHER)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
)
    # BUCLE DEL JUEGO
    while not exit_game:
        # Recibe los valores iniciales (o actuales) de Haskell
        state = haskell_process.stdout.readline().strip()
        if not state:
            break

        # Eliminar espacios adicionales y caracteres no deseados
        state = state.strip().replace("(", "").replace(")", "").strip()
        # Extraer partes separadas por comas
        parts = state.split(",")

        # Obtener estadísticas
        x, y = map(int, parts[:2])
        player_energy = int(parts[2])
        position = (x, y)
        player_hunger = int(parts[3])
        player_thirst = int(parts[4])
        player_actions = int(parts[5])

        # Dibujar estado del mapa actual
        draw_map(position, MAP_SIZE, player_energy, opponent_energy, player_actions)

        #Reiniciando estados de posición
        restart_triggers()
        # Cargando estado de posición
        get_triggers_status()

        # Verificando si el jugador realizó alguna acción
        while last_command is None and not exit_game:
            pass

        # Verificando fin del juego
        if exit_game:
            break

        # Verificando si es el turno de la IA
        if last_command == "end_turn":
            AI_Turn()
            change_weather()

        # Cargando nuevo estado de juego en Haskell para su procesamiento
        haskell_process.stdin.write(last_command + "\n")
        haskell_process.stdin.flush()
        last_command = None

        # Condiciones de VICTORIA/DERROTA
        if player_energy <= 0 or player_hunger <= 0 or player_thirst <= 0:
            show_game_over()
            break

        # Esperando tiempo de refrescado antes de volver a cargar el ciclo
        time.sleep(MOVE_DELAY)

except KeyboardInterrupt:
    print("Juego terminado.")
    time.sleep(1)
finally:
    listener.stop()
    haskell_process.terminate()
    print("\nGracias por jugar!")