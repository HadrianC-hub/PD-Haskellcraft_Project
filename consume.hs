import System.IO

main :: IO ()
main = do
    input <- getLine
    let (resourceType, weather, energy, hunger, thirst, maxEnergy, maxHunger, maxThirst) = parseInput (words input)
    let (newEnergy, newHunger, newThirst) = consumeResource resourceType weather energy hunger thirst maxEnergy maxHunger maxThirst
    putStrLn $ show newEnergy ++ " " ++ show newHunger ++ " " ++ show newThirst

-- Parsear entrada desde Python
parseInput :: [String] -> (String, Int, Int, Int, Int, Int, Int, Int)
parseInput (res:w:e:h:t:maxE:maxH:maxT:_) = (res, read w, read e, read h, read t, read maxE, read maxH, read maxT)
parseInput _ = ("", 0, 0, 0, 0, 0, 0, 0)

-- Lógica para consumir el recurso con límites
consumeResource :: String -> Int -> Int -> Int -> Int -> Int -> Int -> Int -> (Int, Int, Int)
consumeResource "wood" _ energy hunger thirst maxEnergy _ _ = (min maxEnergy (energy + 10), hunger, thirst)
consumeResource "water" 2 energy hunger thirst _ _ maxThirst = (energy, hunger, min maxThirst (thirst + 10))  -- Clima lluvioso
consumeResource "water" _ energy hunger thirst _ _ maxThirst = (energy, hunger, min maxThirst (thirst + 5))
consumeResource "food" 4 energy hunger thirst _ maxHunger _ = (energy, min maxHunger (hunger + 5), thirst)    -- Clima frío
consumeResource "food" _ energy hunger thirst _ maxHunger _ = (energy, min maxHunger (hunger + 10), thirst)
consumeResource _ _ energy hunger thirst _ _ _ = (energy, hunger, thirst)  -- Caso por defecto