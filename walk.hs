import System.IO

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    loop
-- Bucle
loop :: IO ()
loop = do
    input <- getLine
    if input == "exit" 
        then return ()
        else do
            let (weather, energy, hunger, thirst) = parseInput (words input)
            let (newEnergy, newHunger, newThirst) = applyMovementEffects weather energy hunger thirst
            putStrLn $ show newEnergy ++ " " ++ show newHunger ++ " " ++ show newThirst
            loop  -- Vuelve a esperar entrada
-- Parsear entrada
parseInput :: [String] -> (Int, Int, Int, Int)
parseInput (w:e:h:t:_) = (read w, read e, read h, read t)
parseInput _ = error "Formato incorrecto"
-- Calcular costo de caminar en dependencia del día
applyMovementEffects :: Int -> Int -> Int -> Int -> (Int, Int, Int)
applyMovementEffects weather energy hunger thirst =
    let energyCost = if weather == 1 || weather == 4 then 2 else 1
        thirstCost = if weather == 1 then 2 else 1
    in (max 0 (energy - energyCost), max 0 (hunger - 1), max 0 (thirst - thirstCost))