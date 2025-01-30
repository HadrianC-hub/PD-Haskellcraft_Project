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

