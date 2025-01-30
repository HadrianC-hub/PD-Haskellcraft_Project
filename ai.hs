import System.IO
import Data.List (minimumBy)
import Data.Ord (comparing)

type Position = (Int, Int)

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering  -- Asegura salida inmediata
    loop

loop :: IO ()
loop = do
    input <- getLine
    if null input
        then loop  -- Si la entrada está vacía, volver a esperar
        else do
            let values = words input
            case parseInput values of
                Left err -> do
                    putStrLn err
                    hFlush stdout  -- Asegurar que el error se envíe antes de continuar
                    loop
                Right (wood, water, food, opponentPos, campPos) -> do
                    let target = decideTarget wood water food opponentPos campPos
                    printPosition target
                    hFlush stdout  -- Asegurar salida antes de seguir
                    loop

-- Parsear entrada recibida desde Python
parseInput :: [String] -> Either String ([Position], [Position], [Position], Position, Position)
parseInput values = do
    let readPairs [] = []
        readPairs (x:y:rest) = (read x, read y) : readPairs rest
        readPairs _ = error "Formato de entrada incorrecto"

    case values of
        (woodCountStr:rest1) -> do
            let woodCount = read woodCountStr
            let (woodPosStr, rest2) = splitAt (2 * woodCount) rest1
            let wood = readPairs woodPosStr

            case rest2 of
                (waterCountStr:rest3) -> do
                    let waterCount = read waterCountStr
                    let (waterPosStr, rest4) = splitAt (2 * waterCount) rest3
                    let water = readPairs waterPosStr

                    case rest4 of
                        (foodCountStr:rest5) -> do
                            let foodCount = read foodCountStr
                            let (foodPosStr, rest6) = splitAt (2 * foodCount) rest5
                            let food = readPairs foodPosStr

                            case rest6 of
                                (opX:opY:campX:campY:_) ->
                                    Right (wood, water, food, (read opX, read opY), (read campX, read campY))
                                _ -> Left "Error: No hay suficientes datos para la posición del oponente y campamento"
                        _ -> Left "Error: No hay suficientes datos para la comida"
                _ -> Left "Error: No hay suficientes datos para el agua"
        _ -> Left "Error: Entrada vacía"

-- Seleccionar el recurso más cercano o volver al campamento si no hay recursos
decideTarget :: [Position] -> [Position] -> [Position] -> Position -> Position -> Position
decideTarget wood water food opponentPos campPos
    | null allResources = campPos  -- Si no hay recursos, volver al campamento
    | otherwise = minimumBy (comparing (manhattanDistance opponentPos)) allResources
  where
    allResources = wood ++ water ++ food

-- Calcular distancia de Manhattan
manhattanDistance :: Position -> Position -> Int
manhattanDistance (x1, y1) (x2, y2) = abs (x1 - x2) + abs (y1 - y2)

-- Imprimir la posición objetivo
printPosition :: Position -> IO ()
printPosition (x, y) = putStrLn (show x ++ " " ++ show y)