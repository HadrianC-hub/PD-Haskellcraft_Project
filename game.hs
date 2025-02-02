import System.Environment (getArgs)
import System.IO

-- Tipo de estado del juego
type Position = (Int, Int)
type GameState = (Position, Int, Int, Int, Int)  
-- (Actual_Position, Actual_Energy, Actual_Hunger, Actual_Thirst, Actual_Actions)

-- Configuración del juego
data GameConfig = GameConfig
    { mapSize       :: Int
    , initialEnergy :: Int
    , initialHunger :: Int
    , initialThirst :: Int
    , initialActions :: Int
    , player1Start  :: Position
    , player2Start  :: Position
    , actualWeather :: Int  -- Nuevo: Estado del clima
    }

-- Lógica principal del juego
main :: IO ()
main = do
    args <- getArgs
    let config = case args of
            (n:e:h:t:a:x1:y1:x2:y2:w:_) -> GameConfig (read n) (read e) (read h) (read t) (read a) (read x1, read y1) (read x2, read y2) (read w)
            (n:e:h:t:a:x1:y1:x2:y2:_)   -> GameConfig (read n) (read e) (read h) (read t) (read a) (read x1, read y1) (read x2, read y2) 0
            (n:e:h:t:a:x1:y1:_)         -> GameConfig (read n) (read e) (read h) (read t) (read a) (read x1, read y1) (0,0) 0
            (n:e:h:t:a:_)               -> GameConfig (read n) (read e) (read h) (read t) (read a) (0,0) (0,0) 0
            _                           -> GameConfig 10 100 50 50 3 (0,0) (0,0) 0

    -- Iniciar el juego con la posición inicial del primer jugador
    gameLoop config (actualWeather config) (player1Start config, initialEnergy config, initialHunger config, initialThirst config, initialActions config)

-- Bucle principal del juego
gameLoop :: GameConfig -> Int -> GameState -> IO ()
gameLoop config currentWeather state@((x, y), energy, hunger, thirst, actions) = do
    -- Mostrar estado actual con clima actualizado
    putStrLn $ show (x, y, energy, hunger, thirst, actions, currentWeather)
    hFlush stdout  -- Asegurar salida inmediata

    -- Leer comando del usuario
    command <- getLine

    -- Solo actualizar el clima si se recibe el comando adecuado
    newWeather <-
        if command == "change_weather"
            then do
                newWeatherStr <- getLine
                return (read newWeatherStr :: Int)
            else return currentWeather

    -- Actualizar estado
    let newState = updateState config newWeather command state

    -- Llamada recursiva con el nuevo clima
    gameLoop config newWeather newState

-- Actualización del estado del juego según el clima
updateState :: GameConfig -> Int -> String -> GameState -> GameState
updateState config weather command ((x, y), energy, hunger, thirst, actions) =
    let movementCost = case weather of
            1 -> 2  -- Soleado: el movimiento cuesta el doble de energía y sed
            4 -> 2  -- Frío: el movimiento cuesta el doble de energía
            _ -> 1  -- Normal

        newPosition = case command of
            "up"    -> (x, max 0 (y - 1))
            "down"  -> (x, min (mapSize config - 1) (y + 1))
            "left"  -> (max 0 (x - 1), y)
            "right" -> (min (mapSize config - 1) (x + 1), y)
            _       -> (x, y)

        energyAfterMove = if newPosition /= (x, y) then max 0 (energy - movementCost) else energy
        hungerAfterMove = if newPosition /= (x, y) then max 0 (hunger - 1) else hunger
        thirstAfterMove = if newPosition /= (x, y) then max 0 (thirst - (if weather == 1 then 2 else 1)) else thirst

        -- Actualizar cantidad de acciones disponibles si el jugador ejecutó una acción
        newRemainingActions = if command `elem` ["drink_water", "eat_food", "use_wood"] && actions > 0
                then actions - 1
                else actions

        -- Actualizar cantidad de acciones disponibles en dependencia de si se está iniciando un nuevo turno
        newActions = if command == "change_weather" then initialActions config else newRemainingActions

        -- Ajustes según el clima
        newEnergy = if command == "use_wood"
            then min (initialEnergy config) (energyAfterMove + (if weather == 2 then 5 else 10)) -- Lluvia = 5, Normal = 10
            else energyAfterMove

        newHunger = if command == "eat_food"
            then min (initialHunger config) (hungerAfterMove + (if weather == 4 then 5 else 10)) -- Frío = 5, Normal = 10
            else hungerAfterMove

        newThirst = if command == "drink_water"
            then min (initialThirst config) (thirstAfterMove + (if weather == 2 then 10 else if weather == 4 then 3 else 5)) -- Lluvia = 10, Normal = 5
            else thirstAfterMove

    in (newPosition, newEnergy, newHunger, newThirst, newActions)