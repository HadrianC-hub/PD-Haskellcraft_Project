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
    gameLoop config (player1Start config, initialEnergy config, initialHunger config, initialThirst config, initialActions config)

-- Bucle principal del juego
gameLoop :: GameConfig -> GameState -> IO ()
gameLoop config state@((x, y), energy, hunger, thirst, actions) = do
    -- Mostrar estado actual
    putStrLn $ show (x, y, energy, hunger, thirst, actions, actualWeather config)
    hFlush stdout  -- Asegurar salida inmediata
    -- Leer comando del usuario
    command <- getLine
    -- Actualizar estado
    let newState = updateState config command state
    gameLoop config newState

