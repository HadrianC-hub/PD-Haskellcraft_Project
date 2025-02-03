**Desarrollado por:**
- Adrián Hernández Castellanos (C-312)
- Laura Martir Beltrán         (C-311)
- Yesenia Valdés Rodríguez     (C-311)

---

# 🕹️ Juego de Supervivencia en Haskell y Python

## 📖 Descripción
Este es un juego de estrategia y supervivencia en un entorno de mapa bidimensional. El jugador debe recolectar recursos, administrar su energía, hambre y sed, y competir contra una inteligencia artificial (IA) que toma decisiones basadas en su estado y los recursos disponibles en el mapa.

El juego está desarrollado en **Python** para la interfaz y la lógica de control, mientras que **Haskell** maneja la mecánica del juego y la toma de decisiones de la IA.

## 🚀 Características
- 🌍 **Mapa bidimensional** con recursos generados aleatoriamente.
- 🏕️ **Sistema de campamento** donde los jugadores pueden finalizar su turno.
- 🍖 **Consumo de recursos** (agua, comida, madera) con impacto en las estadísticas.
- ☀️ **Sistema de clima dinámico** que afecta el costo de movimiento y el consumo de recursos.
- 🧠 **Inteligencia Artificial (IA)** que toma decisiones estratégicas para maximizar su supervivencia.
- 🔄 **Persistencia de procesos Haskell** para mejorar el rendimiento del juego.

## 📜 Requisitos
- **Python 3.8+**
- **Haskell (GHC 8.10+ y Stack recomendado)**
- **Módulos de Python**:
  - `pynput`
  - `shutil`
  - `subprocess`
  - `random`

Instalar dependencias de Python con:
```bash
pip install pynput
```

## 📂 Estructura del Proyecto
```
/game_project
│── game.hs          # Maneja la lógica del juego
│── ai.hs            # Algoritmo de la IA
│── consume.hs       # Control de consumo de recursos
│── walk.hs          # Manejo del movimiento y su impacto
│── main.py          # Interfaz y control principal en Python
│── README.md        # Documentación del proyecto
```

## 🎮 Cómo Jugar
### **1️⃣ Ejecutar el Juego**
```bash
python main.py
```
### **2️⃣ Controles**
- `↑ ↓ ← →` : Moverse
- `X` : Consumir recurso
- `Q` : Salir del juego
- `Enter` : Confirmar acción

## 🏗️ Funcionamiento Interno
### **🔹 Lógica del Juego** (game.hs)
- Maneja el estado del jugador.
- Controla el impacto del clima en el consumo de recursos.
- Procesa los comandos de movimiento y uso de recursos.

### **🔹 Inteligencia Artificial** (ai.hs)
- Analiza los recursos en el mapa.
- Calcula distancias y asigna prioridades.
- Retorna la mejor acción para la IA.

### **🔹 Consumo de Recursos** (consume.hs)
- Determina cuánta energía, hambre o sed se recupera al consumir un recurso.
- Aplica restricciones según el clima.

### **🔹 Movimiento** (walk.hs)
- Calcula la energía, hambre y sed consumidos al moverse.
- Depende del estado del clima.


## 📜 Licencia
Este proyecto es de código abierto bajo la licencia MIT.

